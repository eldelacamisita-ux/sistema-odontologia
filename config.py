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
        # Render usa postgres://, necesitamos postgresql+psycopg:// para Psycopg 3
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql+psycopg://', 1)
        elif DATABASE_URL.startswith('postgresql://'):
            # Asegurar que use psycopg (Psycopg 3)
            if '+psycopg' not in DATABASE_URL:
                DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)
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
    
    # Deshabilitar emails si no está configurado (útil para testing o cuando no hay servidor SMTP)
    MAIL_SUPPRESS_SEND = not bool(MAIL_USERNAME and MAIL_PASSWORD)
    
    # Configuración de Resend (alternativa moderna para emails)
    RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
    RESEND_FROM_EMAIL = os.environ.get('RESEND_FROM_EMAIL', 'onboarding@resend.dev')
    
    # Información de la clínica
    CLINICA_EMAIL = os.environ.get('CLINICA_EMAIL', 'admin@clinica.com')
    CLINICA_NOMBRE = os.environ.get('CLINICA_NOMBRE', 'Clínica Dental')
    
    # URL base de la aplicación (para enlaces en emails)
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')