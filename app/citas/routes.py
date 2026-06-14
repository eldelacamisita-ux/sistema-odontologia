from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.citas import citas_bp
from app.forms import CitaForm
from app.models import Cita, Paciente
from app.utils import registrar_log

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