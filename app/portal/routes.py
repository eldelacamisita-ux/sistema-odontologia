from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.portal import portal_bp
from app.models import Usuario, Paciente, Cita
from datetime import datetime, date, timedelta

@portal_bp.before_request
@login_required
def verificar_paciente():
    """Middleware para verificar que solo pacientes accedan al portal"""
    if not current_user.es_paciente():
        flash('Acceso denegado. Esta área es solo para pacientes.', 'danger')
        return redirect(url_for('main.index'))

@portal_bp.route('/')
def index():
    """Dashboard del paciente"""
    paciente = current_user.paciente
    if not paciente:
        flash('No se encontró información del paciente', 'warning')
        return redirect(url_for('public.index'))
    
    # Obtener citas del paciente
    citas_proximas = Cita.query.filter(
        Cita.paciente_id == paciente.id,
        Cita.fecha_hora >= datetime.utcnow(),
        Cita.estado.in_(['programada', 'pendiente'])
    ).order_by(Cita.fecha_hora).all()
    
    citas_pasadas = Cita.query.filter(
        Cita.paciente_id == paciente.id,
        Cita.fecha_hora < datetime.utcnow()
    ).order_by(Cita.fecha_hora.desc()).limit(5).all()
    
    return render_template('portal/index.html',
                         paciente=paciente,
                         citas_proximas=citas_proximas,
                         citas_pasadas=citas_pasadas,
                         now=datetime.utcnow)

@portal_bp.route('/mis-citas')
def mis_citas():
    """Ver todas las citas del paciente"""
    paciente = current_user.paciente
    if not paciente:
        flash('No se encontró información del paciente', 'warning')
        return redirect(url_for('public.index'))
    
    citas = Cita.query.filter_by(paciente_id=paciente.id).order_by(Cita.fecha_hora.desc()).all()
    return render_template('portal/mis_citas.html', 
                         citas=citas, 
                         paciente=paciente,
                         now=datetime.utcnow)

@portal_bp.route('/nueva-cita', methods=['GET', 'POST'])
def nueva_cita():
    """Agendar una nueva cita"""
    paciente = current_user.paciente
    if not paciente:
        flash('No se encontró información del paciente', 'warning')
        return redirect(url_for('public.index'))
    
    # Importar HorarioDoctor
    from app.models import HorarioDoctor
    
    # Obtener horarios de la base de datos
    horarios = HorarioDoctor.query.filter_by(activo=True).order_by(
        HorarioDoctor.dia_semana, 
        HorarioDoctor.hora_inicio
    ).all()
    
    # Agrupar por doctor
    doctores = {}
    for h in horarios:
        if h.doctor not in doctores:
            doctores[h.doctor] = []
        doctores[h.doctor].append({
            'dia': h.dia_semana,
            'inicio': h.hora_inicio.strftime('%H:%M'),
            'fin': h.hora_fin.strftime('%H:%M')
        })
    
    if request.method == 'POST':
        try:
            fecha_str = request.form.get('fecha')
            hora_str = request.form.get('hora')
            motivo = request.form.get('motivo')
            doctor_preferido = request.form.get('doctor', '')  # Opcional
            
            # Combinar fecha y hora
            fecha_hora_str = f"{fecha_str} {hora_str}"
            fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
            
            # Verificar que la fecha no sea en el pasado
            if fecha_hora < datetime.utcnow():
                flash('No puedes agendar citas en el pasado', 'danger')
                return redirect(url_for('portal.nueva_cita'))
            
            # Verificar disponibilidad (máximo 5 citas por día)
            fecha_inicio = fecha_hora.replace(hour=0, minute=0, second=0)
            fecha_fin = fecha_hora.replace(hour=23, minute=59, second=59)
            
            citas_del_dia = Cita.query.filter(
                Cita.fecha_hora >= fecha_inicio,
                Cita.fecha_hora <= fecha_fin,
                Cita.estado.in_(['programada', 'pendiente'])
            ).count()
            
            if citas_del_dia >= 5:
                flash('⚠️ Lo sentimos, ese día ya está completo. Por favor selecciona otra fecha.', 'warning')
                return redirect(url_for('portal.nueva_cita'))
            
            # Crear la cita con estado 'pendiente' para aprobación del admin
            admin = Usuario.query.filter_by(rol='odontologo').first()
            if not admin:
                admin = Usuario.query.first()
            
            # Agregar doctor preferido al motivo si se seleccionó
            motivo_completo = motivo
            if doctor_preferido:
                motivo_completo = f"[Doctor preferido: {doctor_preferido}] {motivo}"
            
            nueva = Cita(
                paciente_id=paciente.id,
                usuario_id=admin.id,
                fecha_hora=fecha_hora,
                motivo=motivo_completo,
                estado='pendiente'  # Requiere aprobación del admin
            )
            
            db.session.add(nueva)
            db.session.commit()
            
            # Log de notificación (sin envío de email)
            current_app.logger.info(f"Notificación: Nueva solicitud de cita de {paciente.nombre} para {fecha_hora}")
            
            flash('✅ Solicitud de cita enviada. El consultorio confirmará la disponibilidad en 24 horas.', 'success')
            return redirect(url_for('portal.mis_citas'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agendar la cita: {str(e)}', 'danger')
            return redirect(url_for('portal.nueva_cita'))
    
    # Obtener fechas con disponibilidad para mostrar en el calendario
    fechas_ocupadas = []
    fecha_actual = date.today()
    
    # Revisar los próximos 60 días
    for i in range(60):
        fecha_check = fecha_actual + timedelta(days=i)
        fecha_inicio = datetime.combine(fecha_check, datetime.min.time())
        fecha_fin = datetime.combine(fecha_check, datetime.max.time())
        
        citas_count = Cita.query.filter(
            Cita.fecha_hora >= fecha_inicio,
            Cita.fecha_hora <= fecha_fin,
            Cita.estado.in_(['programada', 'pendiente'])
        ).count()
        
        if citas_count >= 5:
            fechas_ocupadas.append(fecha_check.strftime('%Y-%m-%d'))
    
    return render_template('portal/nueva_cita.html', 
                         paciente=paciente,
                         fecha_hoy=date.today().strftime('%Y-%m-%d'),
                         fechas_ocupadas=fechas_ocupadas,
                         doctores=doctores)

@portal_bp.route('/mi-perfil', methods=['GET', 'POST'])
def mi_perfil():
    """Ver y editar perfil del paciente"""
    paciente = current_user.paciente
    if not paciente:
        flash('No se encontró información del paciente', 'warning')
        return redirect(url_for('public.index'))
    
    if request.method == 'POST':
        try:
            paciente.telefono = request.form.get('telefono')
            paciente.direccion = request.form.get('direccion')
            
            fecha_nac_str = request.form.get('fecha_nacimiento')
            if fecha_nac_str:
                paciente.fecha_nacimiento = datetime.strptime(fecha_nac_str, '%Y-%m-%d').date()
            
            db.session.commit()
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('portal.mi_perfil'))
            
        except Exception as e:
            flash(f'Error al actualizar el perfil: {str(e)}', 'danger')
    
    return render_template('portal/mi_perfil.html', paciente=paciente, usuario=current_user)

@portal_bp.route('/cancelar-cita/<int:cita_id>')
def cancelar_cita(cita_id):
    """Cancelar una cita"""
    paciente = current_user.paciente
    if not paciente:
        flash('No se encontró información del paciente', 'warning')
        return redirect(url_for('public.index'))
    
    cita = Cita.query.get_or_404(cita_id)
    
    # Verificar que la cita pertenece al paciente
    if cita.paciente_id != paciente.id:
        flash('No tienes permiso para cancelar esta cita', 'danger')
        return redirect(url_for('portal.mis_citas'))
    
    # Solo se pueden cancelar citas futuras
    if cita.fecha_hora < datetime.utcnow():
        flash('No puedes cancelar citas pasadas', 'danger')
        return redirect(url_for('portal.mis_citas'))
    
    cita.estado = 'cancelada'
    db.session.commit()
    
    flash('Cita cancelada exitosamente', 'success')
    return redirect(url_for('portal.mis_citas'))
