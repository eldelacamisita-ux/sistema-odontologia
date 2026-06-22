from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.citas import citas_bp
from app.forms import CitaForm
from app.models import Cita, Paciente, ComprobantePago
from app.utils import registrar_log, rol_requerido
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/static/comprobantes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@citas_bp.route('/')
@login_required
def listar():
    citas = Cita.query.order_by(Cita.fecha_hora).all()
    return render_template('citas/listar.html', citas=citas)

@citas_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    form = CitaForm()
    form.paciente_id.choices = [(p.id, p.nombre) for p in Paciente.query.all()]
    if form.validate_on_submit():
        fecha_hora = datetime.combine(form.fecha.data, datetime.strptime(form.hora.data, '%H:%M').time())
        cita = Cita(
            paciente_id=form.paciente_id.data,
            usuario_id=current_user.id,
            fecha_hora=fecha_hora,
            motivo=form.motivo.data,
            estado=form.estado.data
        )
        db.session.add(cita)
        db.session.commit()
        registrar_log(f'Agendó cita para paciente ID {cita.paciente_id}', 'cita', cita.id)
        flash('Cita agendada correctamente', 'success')
        return redirect(url_for('citas.listar'))
    return render_template('citas/formulario.html', form=form)

@citas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    cita = Cita.query.get_or_404(id)
    form = CitaForm(obj=cita)
    form.paciente_id.choices = [(p.id, p.nombre) for p in Paciente.query.all()]
    if form.validate_on_submit():
        cita.paciente_id = form.paciente_id.data
        fecha_hora = datetime.combine(form.fecha.data, datetime.strptime(form.hora.data, '%H:%M').time())
        cita.fecha_hora = fecha_hora
        cita.motivo = form.motivo.data
        cita.estado = form.estado.data
        db.session.commit()
        registrar_log(f'Editó cita ID {id}', 'cita', id)
        flash('Cita actualizada', 'success')
        return redirect(url_for('citas.listar'))
    # Prellenar campos
    form.fecha.data = cita.fecha_hora.date()
    form.hora.data = cita.fecha_hora.strftime('%H:%M')
    form.estado.data = cita.estado
    return render_template('citas/formulario.html', form=form, cita=cita)

@citas_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    cita = Cita.query.get_or_404(id)
    db.session.delete(cita)
    db.session.commit()
    registrar_log(f'Eliminó cita ID {id}', 'cita', id)
    flash('Cita cancelada', 'warning')
    return redirect(url_for('citas.listar'))


@citas_bp.route('/subir-comprobante/<int:cita_id>', methods=['GET', 'POST'])
@login_required
def subir_comprobante(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    # Solo el paciente dueño de la cita o el admin puede subir
    if current_user.rol != 'odontologo' and current_user.paciente_id != cita.paciente_id:
        abort(403)
    
    if request.method == 'POST':
        if 'foto' not in request.files:
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)
        file = request.files['foto']
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Formato no permitido. Use PNG, JPG, JPEG, GIF o PDF.', 'danger')
            return redirect(request.url)
        
        # Crear carpeta si no existe
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(f"cita_{cita_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Guardar en base de datos con procedimiento y tipo_paciente
        comprobante = ComprobantePago(
            cita_id=cita_id,
            paciente_id=cita.paciente_id,
            monto=float(request.form.get('monto', 0)),
            foto_path=filepath,
            estado='pendiente',
            procedimiento=request.form.get('procedimiento'),
            tipo_paciente=request.form.get('tipo_paciente')
        )
        db.session.add(comprobante)
        db.session.commit()
        registrar_log(f'Subió comprobante de pago para cita ID {cita_id}', 'comprobantepago', comprobante.id)
        flash('✅ Comprobante subido correctamente. Espera la aprobación.', 'success')
        return redirect(url_for('citas.listar'))
    
    return render_template('citas/subir_comprobante.html', cita=cita)

@citas_bp.route('/comprobantes/pendientes')
@login_required
@rol_requerido('odontologo')
def comprobantes_pendientes():
    comprobantes = ComprobantePago.query.filter_by(estado='pendiente').all()
    return render_template('citas/comprobantes_pendientes.html', comprobantes=comprobantes)

@citas_bp.route('/comprobantes/aprobar/<int:id>', methods=['POST'])
@login_required
@rol_requerido('odontologo')
def aprobar_comprobante(id):
    comprobante = ComprobantePago.query.get_or_404(id)
    comprobante.estado = 'aprobado'
    db.session.commit()
    registrar_log(f'Aprobó comprobante ID {id}', 'comprobantepago', id)
    flash('Comprobante aprobado', 'success')
    return redirect(url_for('citas.comprobantes_pendientes'))

@citas_bp.route('/comprobantes/rechazar/<int:id>', methods=['POST'])
@login_required
@rol_requerido('odontologo')
def rechazar_comprobante(id):
    comprobante = ComprobantePago.query.get_or_404(id)
    comprobante.estado = 'rechazado'
    comprobante.observaciones = request.form.get('observaciones', '')
    db.session.commit()
    registrar_log(f'Rechazó comprobante ID {id}: {comprobante.observaciones}', 'comprobantepago', id)
    flash('Comprobante rechazado', 'warning')
    return redirect(url_for('citas.comprobantes_pendientes'))

@citas_bp.route('/pagos')
@login_required
def listar_pagos():
    """Panel de pagos - Solo admin/odontólogo puede ver"""
    if current_user.rol != 'odontologo':
        flash('No tienes permiso para ver esta sección', 'danger')
        return redirect(url_for('main.index'))
    
    from app.models import Precio
    comprobantes = ComprobantePago.query.order_by(ComprobantePago.fecha_subida.desc()).all()
    
    # Calcular precio esperado para cada comprobante
    for c in comprobantes:
        if c.procedimiento and c.tipo_paciente:
            precio = Precio.query.filter_by(
                procedimiento=c.procedimiento,
                tipo_paciente=c.tipo_paciente
            ).first()
            c.precio_esperado = precio.precio if precio else None
        else:
            c.precio_esperado = None
    
    return render_template('citas/pagos.html', comprobantes=comprobantes)

@citas_bp.route('/pagos/confirmar/<int:id>', methods=['POST'])
@login_required
def confirmar_pago(id):
    """Confirmar pago definitivamente"""
    if current_user.rol != 'odontologo':
        flash('No tienes permiso', 'danger')
        return redirect(url_for('main.index'))
    
    comprobante = ComprobantePago.query.get_or_404(id)
    comprobante.estado = 'confirmado'
    db.session.commit()
    registrar_log(f'Confirmó pago ID {id}', 'comprobantepago', id)
    flash('✅ Pago confirmado correctamente', 'success')
    return redirect(url_for('citas.listar_pagos'))
