"""
Configuración de la aplicación Flask
Soporta SQLite para desarrollo local y PostgreSQL para producción
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración principal de la aplicación"""
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    FERNET_KEY = os.environ.get('FERNET_KEY', '')
    
    # Base de datos: PostgreSQL en producción (Render), SQLite en local
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Render usa postgres://, SQLAlchemy necesita postgresql://
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # SQLite para desarrollo local
        SQLALCHEMY_DATABASE_URI = 'sqlite:///odontologia.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_USERNAME'))
    
    # Información de la clínica
    CLINICA_EMAIL = os.environ.get('CLINICA_EMAIL', 'admin@clinica.com')
    CLINICA_NOMBRE = os.environ.get('CLINICA_NOMBRE', 'Clínica Dental')
    
    # URL base de la aplicación (para enlaces en emails)
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')