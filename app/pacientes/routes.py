from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.pacientes import pacientes_bp
from app.forms import PacienteForm, NotaClinicaForm
from app.models import Paciente, NotaClinica, Odontograma
from app.utils import registrar_log, solo_odontologo

@pacientes_bp.route('/')
@login_required
def listar():
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    return render_template('pacientes/listar.html', pacientes=pacientes)

@pacientes_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    form = PacienteForm()
    if form.validate_on_submit():
        paciente = Paciente(
            nombre=form.nombre.data,
            telefono=form.telefono.data,
            email=form.email.data,
            direccion=form.direccion.data,
            fecha_nacimiento=form.fecha_nacimiento.data
        )
        db.session.add(paciente)
        db.session.commit()
        registrar_log(f'Creó paciente {paciente.nombre}', 'paciente', paciente.id)
        flash('Paciente registrado correctamente', 'success')
        return redirect(url_for('pacientes.listar'))
    return render_template('pacientes/formulario.html', form=form)

@pacientes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    paciente = Paciente.query.get_or_404(id)
    form = PacienteForm(obj=paciente)
    if form.validate_on_submit():
        form.populate_obj(paciente)
        db.session.commit()
        registrar_log(f'Editó paciente {paciente.nombre}', 'paciente', paciente.id)
        flash('Paciente actualizado', 'success')
        return redirect(url_for('pacientes.listar'))
    return render_template('pacientes/formulario.html', form=form, paciente=paciente)

@pacientes_bp.route('/eliminar/<int:id>')
@login_required
@solo_odontologo
def eliminar(id):
    paciente = Paciente.query.get_or_404(id)
    nombre = paciente.nombre
    db.session.delete(paciente)
    db.session.commit()
    registrar_log(f'Eliminó paciente {nombre}', 'paciente', id)
    flash('Paciente eliminado', 'warning')
    return redirect(url_for('pacientes.listar'))

@pacientes_bp.route('/historia/<int:id>')
@login_required
def historia(id):
    paciente = Paciente.query.get_or_404(id)
    notas = NotaClinica.query.filter_by(paciente_id=id).order_by(NotaClinica.fecha.desc()).all()
    # Descifrar
    for n in notas:
        n.patologias_text = n.get_patologias()
        n.tratamiento_text = n.get_tratamiento()
        n.observaciones_text = n.get_observaciones()
    return render_template('pacientes/historia.html', paciente=paciente, notas=notas)

@pacientes_bp.route('/historia/nueva/<int:paciente_id>', methods=['POST'])
@login_required
@solo_odontologo
def nueva_nota(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    patologias = request.form.get('patologias', '')
    tratamiento = request.form.get('tratamiento', '')
    observaciones = request.form.get('observaciones', '')
    nota = NotaClinica(paciente_id=paciente_id, usuario_id=current_user.id)
    nota.set_patologias(patologias)
    nota.set_tratamiento(tratamiento)
    nota.set_observaciones(observaciones)
    db.session.add(nota)
    db.session.commit()
    registrar_log(f'Añadió nota clínica a {paciente.nombre}', 'nota_clinica', nota.id)
    flash('Nota clínica agregada (datos cifrados)', 'success')
    return redirect(url_for('pacientes.historia', id=paciente_id))

@pacientes_bp.route('/odontograma/<int:paciente_id>', methods=['GET', 'POST'])
@login_required
def odontograma(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    odonto = Odontograma.query.filter_by(paciente_id=paciente_id).first()
    if not odonto:
        odonto = Odontograma(paciente_id=paciente_id, dientes={})
        db.session.add(odonto)
        db.session.commit()
    if request.method == 'POST':
        if current_user.rol != 'odontologo':
            abort(403)
        # El formulario envía un JSON en un campo oculto "dientes_json"
        import json
        dientes_data = request.form.get('dientes_json', '{}')
        try:
            dientes = json.loads(dientes_data)
        except:
            dientes = {}
        odonto.dientes = dientes
        db.session.commit()
        registrar_log(f'Actualizó odontograma de {paciente.nombre}', 'odontograma', paciente_id)
        flash('Odontograma guardado', 'success')
        return redirect(url_for('pacientes.odontograma', paciente_id=paciente_id))
    # Lista de dientes según FDI (11-18,21-28,31-38,41-48)
    dientes_list = [str(i) for i in range(11,19)] + [str(i) for i in range(21,29)] + \
                   [str(i) for i in range(31,39)] + [str(i) for i in range(41,49)]
    estados = {
        'sano': {'icono':'🟢', 'texto':'Sano'},
        'caries': {'icono':'🔴', 'texto':'Caries'},
        'tratado': {'icono':'🟡', 'texto':'Tratado'},
        'extraido': {'icono':'⚪', 'texto':'Extraído'}
    }
    return render_template('odontograma.html', paciente=paciente, dientes_list=dientes_list,
                           estados=estados, actual=odonto.dientes)