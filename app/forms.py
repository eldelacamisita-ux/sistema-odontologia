from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])

class RegistroForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    rol = SelectField('Rol', choices=[('recepcionista', 'Recepcionista'), ('odontologo', 'Odontólogo')], validators=[DataRequired()])

class RegistroPacienteForm(FlaskForm):
    """Formulario de registro para pacientes"""
    nombre = StringField('Nombre completo', validators=[DataRequired(), Length(min=3, max=100)])
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=10)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')])

class PacienteForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[DataRequired()])
    telefono = StringField('Teléfono')
    email = StringField('Email', validators=[Optional(), Email()])
    direccion = StringField('Dirección')
    fecha_nacimiento = DateField('Fecha de nacimiento', validators=[Optional()])

class CitaForm(FlaskForm):
    paciente_id = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    fecha = DateField('Fecha', validators=[DataRequired()])
    hora = StringField('Hora (HH:MM)', validators=[DataRequired()])
    motivo = StringField('Motivo')
    estado = SelectField('Estado', choices=[
        ('pendiente', 'Pendiente'),
        ('programada', 'Confirmada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
        ('rechazada', 'Rechazada')
    ], default='programada')

class NotaClinicaForm(FlaskForm):
    patologias = TextAreaField('Patologías diagnosticadas')
    tratamiento = TextAreaField('Tratamiento indicado')
    observaciones = TextAreaField('Observaciones y evolución')