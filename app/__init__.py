from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder.'

    from app.models import Usuario
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar blueprints - ORDEN IMPORTANTE
    from app.public import public_bp
    from app.auth import auth_bp
    from app.portal import portal_bp
    from app.main import main_bp
    from app.pacientes import pacientes_bp
    from app.citas import citas_bp

    # Exentar CSRF para el blueprint público
    csrf.exempt(public_bp)

    # Registrar en orden: público primero (sin prefijo)
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(portal_bp)  # Portal de pacientes en /portal
    app.register_blueprint(main_bp, url_prefix='/dashboard')
    app.register_blueprint(pacientes_bp, url_prefix='/pacientes')
    app.register_blueprint(citas_bp, url_prefix='/citas')

    # Crear tablas y usuario admin
    with app.app_context():
        db.create_all()
        from app.models import Usuario, HorarioDoctor
        from datetime import time
        
        # Crear usuario admin si no existe
        if not Usuario.query.filter_by(username='admin').first():
            admin = Usuario(username='admin', email='admin@clinica.com', rol='odontologo')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuario admin creado: admin / admin123")
        
        # Seed de horarios si no existen
        if not HorarioDoctor.query.first():
            horarios = [
                HorarioDoctor(doctor="Dr. Nelson Rodriguez", dia_semana="Lunes", hora_inicio=time(12, 0), hora_fin=time(15, 0)),
                HorarioDoctor(doctor="Dr. Nelson Rodriguez", dia_semana="Miércoles", hora_inicio=time(12, 0), hora_fin=time(15, 0)),
                HorarioDoctor(doctor="Dra. Werllith Rangel", dia_semana="Martes", hora_inicio=time(8, 0), hora_fin=time(11, 0)),
                HorarioDoctor(doctor="Dra. Werllith Rangel", dia_semana="Jueves", hora_inicio=time(8, 0), hora_fin=time(11, 0)),
            ]
            db.session.add_all(horarios)
            db.session.commit()
            print("✅ Horarios iniciales creados")

    # Ruta de debug
    @app.route('/debug')
    def debug():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.endpoint}: {rule.rule}")
        return "<br>".join(routes)

    return app
