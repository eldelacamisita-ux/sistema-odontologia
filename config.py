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
    
    # Información de la clínica
    CLINICA_NOMBRE = os.environ.get('CLINICA_NOMBRE', 'Clínica Dental')
    
    # Configuración de carga de archivos
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/static/uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB máximo