from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from app.main import main_bp
from app.models import Cita, Paciente, LogAuditoria
from app.utils import rol_requerido, registrar_log
from sqlalchemy import func, extract

@main_bp.route('/')
@login_required
def index():
    from app.models import HorarioDoctor
    
    ahora = datetime.utcnow()
    limite = ahora + timedelta(hours=48)
    citas_proximas = Cita.query.filter(
        Cita.fecha_hora >= ahora,
        Cita.fecha_hora <= limite,
        Cita.estado == 'programada'
    ).order_by(Cita.fecha_hora).all()
    
    # Contar solicitudes pendientes (pacientes registrados)
    solicitudes_pendientes = Cita.query.filter_by(estado='pendiente').count()
    
    # Contar solicitudes públicas (sin registro)
    from app.models import CitaPublica
    solicitudes_publicas = CitaPublica.query.filter_by(atendido=False).count()
    
    total_pacientes = Paciente.query.count()
    
    # Contar citas de hoy - Compatible con PostgreSQL y SQLite
    inicio_hoy = datetime(ahora.year, ahora.month, ahora.day)
    fin_hoy = inicio_hoy + timedelta(days=1)
    total_citas_hoy = Cita.query.filter(
        Cita.fecha_hora >= inicio_hoy,
        Cita.fecha_hora < fin_hoy
    ).count()

    # Citas por día de la semana - Compatible con PostgreSQL y SQLite
    # EXTRACT('dow', ...) devuelve 0=Domingo, 1=Lunes, ..., 6=Sábado
    citas_por_dia = db.session.query(
        extract('dow', Cita.fecha_hora).label('dia'),
        func.count(Cita.id).label('total')
    ).group_by('dia').all()
    # Mapeo de días: 0=Dom, 1=Lun, 2=Mar, 3=Mié, 4=Jue, 5=Vie, 6=Sáb
    dias_map = {0:'Dom', 1:'Lun', 2:'Mar', 3:'Mié', 4:'Jue', 5:'Vie', 6:'Sáb'}
    
    # Convertir resultados a formato de gráfico
    chart_data = []
    for d in citas_por_dia:
        if d[0] is not None:
            # d[0] puede ser int, Decimal o string dependiendo de la BD
            dia_num = int(d[0])
            chart_data.append({'dia': dias_map.get(dia_num, str(dia_num)), 'total': d[1]})
    
    # Obtener horarios para mostrar en el dashboard
    horarios = HorarioDoctor.query.filter_by(activo=True).order_by(HorarioDoctor.dia_semana).all()

    return render_template('index.html',
                           citas_proximas=citas_proximas,
                           solicitudes_pendientes=solicitudes_pendientes,
                           solicitudes_publicas=solicitudes_publicas,
                           total_pacientes=total_pacientes,
                           total_citas_hoy=total_citas_hoy,
                           chart_data=chart_data,
                           horarios=horarios)

@main_bp.route('/solicitudes-pendientes')
@login_required
@rol_requerido('odontologo', 'recepcionista')
def solicitudes_pendientes():
    """Ver todas las solicitudes de citas pendientes de aprobación"""
    solicitudes = Cita.query.filter_by(estado='pendiente').order_by(Cita.created_at.desc()).all()
    
    # Calcular citas confirmadas por día para cada solicitud
    contadores_dia = {}
    for cita in solicitudes:
        fecha_str = cita.fecha_hora.date().isoformat()
        
        if fecha_str not in contadores_dia:
            # Contar citas confirmadas ese día
            fecha_inicio = cita.fecha_hora.replace(hour=0, minute=0, second=0, microsecond=0)
            fecha_fin = cita.fecha_hora.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            count = Cita.query.filter(
                Cita.fecha_hora >= fecha_inicio,
                Cita.fecha_hora <= fecha_fin,
                Cita.estado == 'programada'
            ).count()
            
            contadores_dia[fecha_str] = count
    
    return render_template('solicitudes_pendientes.html', 
                         solicitudes=solicitudes,
                         contadores_dia=contadores_dia)

@main_bp.route('/solicitudes-publicas')
@login_required
@rol_requerido('odontologo', 'recepcionista')
def solicitudes_publicas():
    """Ver todas las solicitudes públicas (sin registro)"""
    from app.models import CitaPublica
    solicitudes = CitaPublica.query.filter_by(atendido=False).order_by(CitaPublica.fecha_solicitud.desc()).all()
    return render_template('solicitudes_publicas.html', solicitudes=solicitudes)

@main_bp.route('/marcar-solicitud-atendida/<int:solicitud_id>', methods=['POST'])
@login_required
@rol_requerido('odontologo', 'recepcionista')
def marcar_solicitud_atendida(solicitud_id):
    """Marcar una solicitud pública como atendida"""
    from app.models import CitaPublica
    solicitud = CitaPublica.query.get_or_404(solicitud_id)
    
    solicitud.atendido = True
    db.session.commit()
    
    registrar_log(f'Marcó solicitud pública ID {solicitud_id} ({solicitud.nombre}) como atendida', 'citapublica', solicitud_id)
    flash(f'✅ Solicitud de {solicitud.nombre} marcada como atendida', 'success')
    
    return redirect(url_for('main.solicitudes_publicas'))

@main_bp.route('/aprobar-cita/<int:cita_id>', methods=['POST'])
@login_required
@rol_requerido('odontologo', 'recepcionista')
def aprobar_cita(cita_id):
    """Aprobar una solicitud de cita"""
    cita = Cita.query.get_or_404(cita_id)
    
    if cita.estado != 'pendiente':
        flash('Esta cita ya fue procesada', 'warning')
        return redirect(url_for('main.solicitudes_pendientes'))
    
    # Verificar disponibilidad nuevamente
    fecha_inicio = cita.fecha_hora.replace(hour=0, minute=0, second=0)
    fecha_fin = cita.fecha_hora.replace(hour=23, minute=59, second=59)
    
    citas_del_dia = Cita.query.filter(
        Cita.fecha_hora >= fecha_inicio,
        Cita.fecha_hora <= fecha_fin,
        Cita.estado == 'programada'
    ).count()
    
    if citas_del_dia >= 5:
        flash('⚠️ No se puede aprobar: ese día ya tiene 5 citas confirmadas. Sugiere otra fecha al paciente.', 'danger')
        return redirect(url_for('main.solicitudes_pendientes'))
    
    cita.estado = 'programada'
    db.session.commit()
    
    registrar_log(f'Aprobó solicitud de cita ID {cita_id} para {cita.paciente.nombre}', 'cita', cita_id)
    
    # Log de notificación (sin envío de email)
    current_app.logger.info(f"Notificación: Cita confirmada para {cita.paciente.nombre} el {cita.fecha_hora}")
        # No fallar la aprobación si el email falla
    
    flash(f'✅ Cita aprobada para {cita.paciente.nombre} el {cita.fecha_hora.strftime("%d/%m/%Y a las %H:%M")}', 'success')
    
    return redirect(url_for('main.solicitudes_pendientes'))

@main_bp.route('/rechazar-cita/<int:cita_id>', methods=['POST'])
@login_required
@rol_requerido('odontologo', 'recepcionista')
def rechazar_cita(cita_id):
    """Rechazar una solicitud de cita"""
    cita = Cita.query.get_or_404(cita_id)
    
    if cita.estado != 'pendiente':
        flash('Esta cita ya fue procesada', 'warning')
        return redirect(url_for('main.solicitudes_pendientes'))
    
    motivo_rechazo = request.form.get('motivo_rechazo', 'No especificado')
    
    cita.estado = 'rechazada'
    cita.motivo = f"{cita.motivo} [RECHAZADA: {motivo_rechazo}]"
    db.session.commit()
    
    registrar_log(f'Rechazó solicitud de cita ID {cita_id}: {motivo_rechazo}', 'cita', cita_id)
    
    # Log de notificación (sin envío de email)
    current_app.logger.info(f"Notificación: Cita rechazada para {cita.paciente.nombre}. Motivo: {motivo_rechazo}")
        # No fallar el rechazo si el email falla
    
    flash(f'❌ Solicitud rechazada para {cita.paciente.nombre}', 'warning')
    
    return redirect(url_for('main.solicitudes_pendientes'))

@main_bp.route('/logs')
@login_required
@rol_requerido('odontologo')
def ver_logs():
    logs = LogAuditoria.query.order_by(LogAuditoria.fecha.desc()).limit(200).all()
    return render_template('logs.html', logs=logs)

@main_bp.route('/agentes')
@login_required
@rol_requerido('odontologo')
def panel_agentes():
    """Panel de control para los agentes autónomos"""
    from planificador_agentes import obtener_planificador
    
    planificador = obtener_planificador()
    trabajos = []
    
    if planificador:
        trabajos = planificador.listar_trabajos()
    
    return render_template('agentes.html', trabajos=trabajos)

@main_bp.route('/agentes/ejecutar/<agente_id>', methods=['POST'])
@login_required
@rol_requerido('odontologo')
def ejecutar_agente(agente_id):
    """Ejecutar un agente manualmente"""
    from planificador_agentes import obtener_planificador
    
    planificador = obtener_planificador()
    
    if planificador and planificador.ejecutar_ahora(agente_id):
        flash(f'✅ Agente "{agente_id}" programado para ejecución inmediata', 'success')
    else:
        flash(f'❌ No se pudo ejecutar el agente "{agente_id}"', 'danger')
    
    return redirect(url_for('main.panel_agentes'))


@main_bp.route('/horarios')
@login_required
def ver_horarios():
    from app.models import HorarioDoctor
    horarios = HorarioDoctor.query.all()
    return render_template('horarios/listar.html', horarios=horarios)

@main_bp.route('/horarios/nuevo', methods=['GET', 'POST'])
@login_required
@rol_requerido('odontologo')
def nuevo_horario():
    from app.models import HorarioDoctor
    if request.method == 'POST':
        doctor = request.form['doctor']
        dia = request.form['dia']
        hora_inicio = datetime.strptime(request.form['hora_inicio'], '%H:%M').time()
        hora_fin = datetime.strptime(request.form['hora_fin'], '%H:%M').time()
        horario = HorarioDoctor(doctor=doctor, dia_semana=dia, hora_inicio=hora_inicio, hora_fin=hora_fin)
        db.session.add(horario)
        db.session.commit()
        registrar_log(f'Agregó horario: {doctor} - {dia} {hora_inicio}-{hora_fin}', 'horariodoctor', horario.id)
        flash('Horario agregado', 'success')
        return redirect(url_for('main.ver_horarios'))
    return render_template('horarios/formulario.html')

@main_bp.route('/horarios/eliminar/<int:id>')
@login_required
@rol_requerido('odontologo')
def eliminar_horario(id):
    from app.models import HorarioDoctor
    horario = HorarioDoctor.query.get_or_404(id)
    registrar_log(f'Eliminó horario ID {id}', 'horariodoctor', id)
    db.session.delete(horario)
    db.session.commit()
    flash('Horario eliminado', 'warning')
    return redirect(url_for('main.ver_horarios'))


# ==========================================
# 🔔 API PARA NOTIFICACIONES
# ==========================================

@main_bp.route('/api/citas-proximas')
@login_required
def api_citas_proximas():
    """API para obtener citas próximas en las próximas 24 horas"""
    from flask import jsonify
    
    ahora = datetime.utcnow()
    limite = ahora + timedelta(hours=24)  # Próximas 24 horas
    
    # Buscar citas programadas próximas
    citas = Cita.query.filter(
        Cita.fecha_hora >= ahora,
        Cita.fecha_hora <= limite,
        Cita.estado == 'programada'
    ).order_by(Cita.fecha_hora).limit(5).all()  # Máximo 5 citas
    
    return jsonify({
        'citas': [{
            'id': c.id,
            'paciente': c.paciente.nombre if c.paciente else 'Desconocido',
            'fecha': c.fecha_hora.strftime('%d/%m/%Y'),
            'hora': c.fecha_hora.strftime('%H:%M'),
            'motivo': c.motivo
        } for c in citas],
        'total': len(citas)
    })

@main_bp.route('/api/precio', methods=['POST'])
@login_required
def api_precio():
    """API para obtener precio según procedimiento y tipo de paciente"""
    from app.models import Precio
    data = request.get_json()
    procedimiento = data.get('procedimiento')
    tipo_paciente = data.get('tipo_paciente')
    precio = Precio.query.filter_by(
        procedimiento=procedimiento,
        tipo_paciente=tipo_paciente
    ).first()
    return jsonify({'precio': precio.precio if precio else 0})
