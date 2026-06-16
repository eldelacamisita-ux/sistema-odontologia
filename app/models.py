from app import db
from flask_login import UserMixin
from datetime import datetime
from cryptography.fernet import Fernet
from flask import current_app
import bcrypt

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(20), default='paciente')  # Por defecto, los nuevos usuarios son pacientes
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con Paciente
    paciente = db.relationship('Paciente', backref='usuario', uselist=False, foreign_keys=[paciente_id])

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def tiene_acceso_edicion(self):
        return self.rol == 'odontologo'
    
    def es_paciente(self):
        return self.rol == 'paciente'
    
    def es_staff(self):
        return self.rol in ['odontologo', 'recepcionista']

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    fecha_nacimiento = db.Column(db.Date)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    citas = db.relationship('Cita', backref='paciente', lazy=True, cascade='all, delete-orphan')
    notas = db.relationship('NotaClinica', backref='paciente', lazy=True, cascade='all, delete-orphan')
    odontograma = db.relationship('Odontograma', backref='paciente', uselist=False, cascade='all, delete-orphan')

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(200))
    estado = db.Column(db.String(20), default='programada')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario')

class NotaClinica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    patologias_cifrado = db.Column(db.Text)
    tratamiento_cifrado = db.Column(db.Text)
    observaciones_cifrado = db.Column(db.Text)

    usuario = db.relationship('Usuario')

    def _get_fernet(self):
        return Fernet(current_app.config['FERNET_KEY'])

    def set_patologias(self, texto):
        fernet = self._get_fernet()
        self.patologias_cifrado = fernet.encrypt(texto.encode()).decode() if texto else None

    def get_patologias(self):
        if not self.patologias_cifrado:
            return ''
        fernet = self._get_fernet()
        return fernet.decrypt(self.patologias_cifrado.encode()).decode()

    def set_tratamiento(self, texto):
        fernet = self._get_fernet()
        self.tratamiento_cifrado = fernet.encrypt(texto.encode()).decode() if texto else None

    def get_tratamiento(self):
        if not self.tratamiento_cifrado:
            return ''
        fernet = self._get_fernet()
        return fernet.decrypt(self.tratamiento_cifrado.encode()).decode()

    def set_observaciones(self, texto):
        fernet = self._get_fernet()
        self.observaciones_cifrado = fernet.encrypt(texto.encode()).decode() if texto else None

    def get_observaciones(self):
        if not self.observaciones_cifrado:
            return ''
        fernet = self._get_fernet()
        return fernet.decrypt(self.observaciones_cifrado.encode()).decode()

class Odontograma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False, unique=True)
    dientes = db.Column(db.JSON, default=dict)

class LogAuditoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    accion = db.Column(db.String(200))
    tabla_afectada = db.Column(db.String(50))
    registro_id = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(45))

    usuario = db.relationship('Usuario')

class CitaPublica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    fecha_solicitada = db.Column(db.Date)
    mensaje = db.Column(db.Text)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    atendido = db.Column(db.Boolean, default=False)

class HorarioDoctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor = db.Column(db.String(100), nullable=False)  # Ej: "Dr. Nelson Rodriguez"
    dia_semana = db.Column(db.String(20), nullable=False)  # Ej: "Lunes", "Martes", "Miércoles"
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    activo = db.Column(db.Boolean, default=True)

class ComprobantePago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('cita.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    monto = db.Column(db.Float, nullable=False)  # 5 o 10 USD
    foto_path = db.Column(db.String(200), nullable=False)  # Ruta del archivo subido
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, aprobado, rechazado
    observaciones = db.Column(db.String(200))  # Comentario del admin
    
    cita = db.relationship('Cita', backref='comprobante', uselist=False)
    paciente = db.relationship('Paciente', backref='comprobantes')
