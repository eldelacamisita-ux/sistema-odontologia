from functools import wraps
from flask import abort, request
from flask_login import current_user

def rol_requerido(*roles_permitidos):
    """
    Decorador para requerir uno o más roles.
    Uso: @rol_requerido('odontologo') o @rol_requerido('odontologo', 'recepcionista')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if current_user.rol not in roles_permitidos:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def solo_odontologo(f):
    return rol_requerido('odontologo')(f)

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr or '0.0.0.0'

def registrar_log(accion, tabla, registro_id, usuario_id=None):
    from app import db
    from app.models import LogAuditoria
    from flask_login import current_user
    if usuario_id is None and current_user.is_authenticated:
        usuario_id = current_user.id
    log = LogAuditoria(
        usuario_id=usuario_id,
        accion=accion,
        tabla_afectada=tabla,
        registro_id=registro_id,
        ip=get_client_ip()
    )
    db.session.add(log)
    db.session.commit()