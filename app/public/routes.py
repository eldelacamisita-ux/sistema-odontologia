from flask import render_template, request, flash, redirect, url_for
from app import db
from app.public import public_bp
from app.models import CitaPublica
from app.email_utils import enviar_notificacion_solicitud_publica
from datetime import datetime

@public_bp.route('/')
def index():
    return render_template('public/index.html')

@public_bp.route('/test')
def test():
    return "<h1>TEST OK - Blueprint público funciona!</h1>"

@public_bp.route('/solicitar-cita', methods=['POST'])
def solicitar_cita():
    try:
        nombre = request.form.get('nombre', '').strip()
        telefono = request.form.get('telefono', '').strip()
        email = request.form.get('email', '').strip()
        fecha_str = request.form.get('fecha', '').strip()
        mensaje = request.form.get('mensaje', '').strip()
        
        # Validaciones básicas
        if not nombre:
            flash('El nombre es requerido', 'danger')
            return redirect(url_for('public.index') + '#form-cita')
        
        if not telefono:
            flash('El teléfono es requerido', 'danger')
            return redirect(url_for('public.index') + '#form-cita')
        
        # Convertir fecha si existe
        fecha = None
        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de fecha inválido', 'danger')
                return redirect(url_for('public.index') + '#form-cita')
        
        # Crear la solicitud
        nueva = CitaPublica(
            nombre=nombre,
            telefono=telefono,
            email=email if email else None,
            fecha_solicitada=fecha,
            mensaje=mensaje if mensaje else None
        )
        
        db.session.add(nueva)
        db.session.commit()
        
        # Enviar notificación por email al admin
        try:
            enviar_notificacion_solicitud_publica(nueva)
        except Exception as e:
            print(f"Error al enviar email de notificación: {e}")
            # No fallar la solicitud si el email falla
        
        flash('✅ Solicitud de cita enviada exitosamente. Pronto nos comunicaremos con usted.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error al enviar la solicitud: {str(e)}', 'danger')
        print(f"Error en solicitar_cita: {e}")
        import traceback
        traceback.print_exc()
    
    return redirect(url_for('public.index') + '#form-cita')
