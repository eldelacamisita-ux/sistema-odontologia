from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import auth_bp
from app.forms import LoginForm, RegistroForm, RegistroPacienteForm
from app.models import Usuario, Paciente
from app.utils import registrar_log

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirigir según el rol
        if current_user.es_paciente():
            return redirect(url_for('portal.index'))
        else:
            return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            registrar_log('Inicio de sesión', 'auth', user.id, user.id)
            next_page = request.args.get('next')
            
            # Redirigir según el rol
            if not next_page:
                if user.es_paciente():
                    next_page = url_for('portal.index')
                else:
                    next_page = url_for('main.index')
            
            return redirect(next_page)
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro para staff (odontólogos y recepcionistas)"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        if Usuario.query.filter_by(username=form.username.data).first():
            flash('Nombre de usuario ya existe', 'danger')
        elif Usuario.query.filter_by(email=form.email.data).first():
            flash('Email ya registrado', 'danger')
        else:
            user = Usuario(username=form.username.data, email=form.email.data, rol=form.rol.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registro exitoso. Ya puede iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/register-paciente', methods=['GET', 'POST'])
def register_paciente():
    """Registro para pacientes"""
    if current_user.is_authenticated:
        if current_user.es_paciente():
            return redirect(url_for('portal.index'))
        else:
            return redirect(url_for('main.index'))
    
    form = RegistroPacienteForm()
    if form.validate_on_submit():
        if Usuario.query.filter_by(username=form.username.data).first():
            flash('Nombre de usuario ya existe', 'danger')
        elif Usuario.query.filter_by(email=form.email.data).first():
            flash('Email ya registrado', 'danger')
        else:
            try:
                # Crear el registro de Paciente primero
                paciente = Paciente(
                    nombre=form.nombre.data,
                    telefono=form.telefono.data,
                    email=form.email.data
                )
                db.session.add(paciente)
                db.session.flush()  # Para obtener el ID del paciente
                
                # Crear el usuario vinculado al paciente
                user = Usuario(
                    username=form.username.data,
                    email=form.email.data,
                    rol='paciente',
                    paciente_id=paciente.id
                )
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                
                flash('¡Registro exitoso! Ya puedes iniciar sesión y agendar tus citas.', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al registrar: {str(e)}', 'danger')
    
    return render_template('register_paciente.html', form=form)

@auth_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        registrar_log('Cierre de sesión', 'auth', current_user.id, current_user.id)
        logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('public.index'))