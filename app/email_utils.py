"""
Utilidades para envío de emails
"""
from flask import current_app, render_template_string
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    """Enviar email de forma asíncrona"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error al enviar email: {e}")

def send_email(subject, recipients, text_body, html_body=None):
    """
    Enviar un email
    
    Args:
        subject: Asunto del email
        recipients: Lista de destinatarios
        text_body: Cuerpo del mensaje en texto plano
        html_body: Cuerpo del mensaje en HTML (opcional)
    """
    try:
        msg = Message(
            subject=subject,
            recipients=recipients if isinstance(recipients, list) else [recipients],
            body=text_body,
            html=html_body
        )
        
        # Enviar de forma asíncrona para no bloquear la aplicación
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        return True
    except Exception as e:
        print(f"Error al preparar email: {e}")
        return False

def enviar_notificacion_solicitud_publica(solicitud):
    """
    Enviar notificación al admin cuando hay una solicitud pública de cita
    
    Args:
        solicitud: Objeto CitaPublica
    """
    clinica_email = current_app.config.get('CLINICA_EMAIL')
    clinica_nombre = current_app.config.get('CLINICA_NOMBRE')
    base_url = current_app.config.get('BASE_URL')
    
    subject = f"📅 Nueva Solicitud de Cita - {solicitud.nombre}"
    
    text_body = f"""
    Nueva solicitud de cita recibida:
    
    Paciente: {solicitud.nombre}
    Teléfono: {solicitud.telefono}
    Email: {solicitud.email or 'No proporcionado'}
    Fecha preferida: {solicitud.fecha_solicitada.strftime('%d/%m/%Y') if solicitud.fecha_solicitada else 'No especificada'}
    Mensaje: {solicitud.mensaje or 'Sin mensaje'}
    
    Fecha de solicitud: {solicitud.fecha_solicitud.strftime('%d/%m/%Y %H:%M')}
    
    Por favor, revisa la solicitud en: {base_url}/dashboard/solicitudes-publicas
    """
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px;">
                <h2 style="color: #0066cc;">📅 Nueva Solicitud de Cita</h2>
                <hr>
                <p><strong>Paciente:</strong> {solicitud.nombre}</p>
                <p><strong>📞 Teléfono:</strong> <a href="tel:{solicitud.telefono}">{solicitud.telefono}</a></p>
                <p><strong>✉️ Email:</strong> {solicitud.email or 'No proporcionado'}</p>
                <p><strong>📅 Fecha preferida:</strong> {solicitud.fecha_solicitada.strftime('%d/%m/%Y') if solicitud.fecha_solicitada else 'No especificada'}</p>
                <p><strong>💬 Mensaje:</strong><br>{solicitud.mensaje or 'Sin mensaje'}</p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    Solicitud recibida el {solicitud.fecha_solicitud.strftime('%d/%m/%Y a las %H:%M')}
                </p>
                <p style="margin-top: 20px;">
                    <a href="{base_url}/dashboard/solicitudes-publicas" style="background-color: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">
                        Ver Solicitudes Web
                    </a>
                </p>
            </div>
        </body>
    </html>
    """
    
    return send_email(subject, clinica_email, text_body, html_body)

def enviar_notificacion_solicitud_paciente(cita):
    """
    Enviar notificación al admin cuando un paciente registrado solicita cita
    
    Args:
        cita: Objeto Cita
    """
    clinica_email = current_app.config.get('CLINICA_EMAIL')
    base_url = current_app.config.get('BASE_URL')
    
    subject = f"📅 Nueva Solicitud de Cita - {cita.paciente.nombre}"
    
    text_body = f"""
    Nueva solicitud de cita de paciente registrado:
    
    Paciente: {cita.paciente.nombre}
    Teléfono: {cita.paciente.telefono}
    Email: {cita.paciente.email or 'No registrado'}
    Fecha solicitada: {cita.fecha_hora.strftime('%d/%m/%Y %H:%M')}
    Motivo: {cita.motivo or 'No especificado'}
    
    Estado: PENDIENTE DE APROBACIÓN
    
    Revisa en: {base_url}/dashboard/solicitudes-pendientes
    """
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px;">
                <h2 style="color: #0066cc;">📅 Nueva Solicitud de Cita</h2>
                <div style="background-color: #fff3cd; padding: 10px; border-radius: 4px; margin: 10px 0;">
                    <strong>⏰ Estado:</strong> PENDIENTE DE APROBACIÓN
                </div>
                <hr>
                <p><strong>Paciente:</strong> {cita.paciente.nombre}</p>
                <p><strong>📞 Teléfono:</strong> {cita.paciente.telefono}</p>
                <p><strong>✉️ Email:</strong> {cita.paciente.email or 'No registrado'}</p>
                <p><strong>📅 Fecha solicitada:</strong> {cita.fecha_hora.strftime('%d/%m/%Y %H:%M')}</p>
                <p><strong>💬 Motivo:</strong> {cita.motivo or 'No especificado'}</p>
                <hr>
                <p style="margin-top: 20px;">
                    <a href="{base_url}/dashboard/solicitudes-pendientes" style="background-color: #ffc107; color: black; padding: 10px 20px; text-decoration: none; border-radius: 4px;">
                        Ver Solicitudes Pendientes
                    </a>
                </p>
            </div>
        </body>
    </html>
    """
    
    return send_email(subject, clinica_email, text_body, html_body)

def enviar_confirmacion_cita(cita):
    """
    Enviar confirmación al paciente cuando su cita es aprobada
    
    Args:
        cita: Objeto Cita con estado 'programada'
    """
    if not cita.paciente.email:
        print(f"No se puede enviar email: paciente {cita.paciente.nombre} no tiene email")
        return False
    
    clinica_nombre = current_app.config.get('CLINICA_NOMBRE')
    base_url = current_app.config.get('BASE_URL')
    
    subject = f"✅ Cita Confirmada - {clinica_nombre}"
    
    text_body = f"""
    ¡Hola {cita.paciente.nombre}!
    
    Tu cita ha sido CONFIRMADA:
    
    📅 Fecha: {cita.fecha_hora.strftime('%d/%m/%Y')}
    🕐 Hora: {cita.fecha_hora.strftime('%H:%M')}
    🏥 Lugar: {clinica_nombre}
    💬 Motivo: {cita.motivo or 'Consulta general'}
    
    Por favor, llega 10 minutos antes de tu cita.
    
    Si necesitas cancelar o reprogramar, por favor contáctanos con anticipación.
    
    Ver mis citas: {base_url}/portal
    
    ¡Te esperamos!
    
    {clinica_nombre}
    """
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; border: 2px solid #28a745; border-radius: 8px; padding: 20px;">
                <div style="text-align: center; background-color: #28a745; color: white; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                    <h2 style="margin: 0;">✅ ¡Cita Confirmada!</h2>
                </div>
                
                <p>¡Hola <strong>{cita.paciente.nombre}</strong>!</p>
                
                <p>Tu cita ha sido confirmada exitosamente:</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 4px; margin: 20px 0;">
                    <p style="margin: 5px 0;"><strong>📅 Fecha:</strong> {cita.fecha_hora.strftime('%d/%m/%Y')}</p>
                    <p style="margin: 5px 0;"><strong>🕐 Hora:</strong> {cita.fecha_hora.strftime('%H:%M')}</p>
                    <p style="margin: 5px 0;"><strong>🏥 Lugar:</strong> {clinica_nombre}</p>
                    <p style="margin: 5px 0;"><strong>💬 Motivo:</strong> {cita.motivo or 'Consulta general'}</p>
                </div>
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 4px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>⚠️ Importante:</strong> Por favor, llega 10 minutos antes de tu cita.</p>
                </div>
                
                <p>Si necesitas cancelar o reprogramar, por favor contáctanos con anticipación.</p>
                
                <hr>
                
                <p style="text-align: center; margin-top: 20px;">
                    <a href="{base_url}/portal" style="background-color: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">
                        Ver Mis Citas
                    </a>
                </p>
                
                <p style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
                    ¡Te esperamos!<br>
                    <strong>{clinica_nombre}</strong>
                </p>
            </div>
        </body>
    </html>
    """
    
    return send_email(subject, cita.paciente.email, text_body, html_body)

def enviar_rechazo_cita(cita, motivo_rechazo):
    """
    Enviar notificación al paciente cuando su cita es rechazada
    
    Args:
        cita: Objeto Cita con estado 'rechazada'
        motivo_rechazo: Motivo del rechazo
    """
    if not cita.paciente.email:
        print(f"No se puede enviar email: paciente {cita.paciente.nombre} no tiene email")
        return False
    
    clinica_nombre = current_app.config.get('CLINICA_NOMBRE')
    
    subject = f"❌ Solicitud de Cita - {clinica_nombre}"
    
    text_body = f"""
    Hola {cita.paciente.nombre},
    
    Lamentablemente no podemos confirmar tu cita para:
    
    📅 Fecha: {cita.fecha_hora.strftime('%d/%m/%Y')}
    🕐 Hora: {cita.fecha_hora.strftime('%H:%M')}
    
    Motivo: {motivo_rechazo}
    
    Por favor, contáctanos para encontrar otra fecha disponible que se ajuste a tus necesidades.
    
    {clinica_nombre}
    """
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; border: 2px solid #dc3545; border-radius: 8px; padding: 20px;">
                <div style="text-align: center; background-color: #dc3545; color: white; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                    <h2 style="margin: 0;">Solicitud de Cita</h2>
                </div>
                
                <p>Hola <strong>{cita.paciente.nombre}</strong>,</p>
                
                <p>Lamentablemente no podemos confirmar tu cita para:</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 4px; margin: 20px 0;">
                    <p style="margin: 5px 0;"><strong>📅 Fecha solicitada:</strong> {cita.fecha_hora.strftime('%d/%m/%Y')}</p>
                    <p style="margin: 5px 0;"><strong>🕐 Hora solicitada:</strong> {cita.fecha_hora.strftime('%H:%M')}</p>
                </div>
                
                <div style="background-color: #f8d7da; padding: 15px; border-radius: 4px; margin: 20px 0; border-left: 4px solid #dc3545;">
                    <p style="margin: 0;"><strong>Motivo:</strong> {motivo_rechazo}</p>
                </div>
                
                <p>Por favor, contáctanos para encontrar otra fecha disponible que se ajuste a tus necesidades.</p>
                
                <hr>
                
                <p style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
                    <strong>{clinica_nombre}</strong>
                </p>
            </div>
        </body>
    </html>
    """
    
    return send_email(subject, cita.paciente.email, text_body, html_body)
