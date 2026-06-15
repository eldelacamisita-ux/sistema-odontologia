"""
Utilidades para envío de emails con Resend
"""
import resend
from flask import current_app

def send_email_resend(to, subject, html_content):
    """
    Envía un correo usando Resend
    
    Args:
        to: Email del destinatario (string)
        subject: Asunto del email
        html_content: Contenido HTML del email
    
    Returns:
        bool: True si se envió correctamente, False si hubo error
    """
    api_key = current_app.config.get('RESEND_API_KEY')
    if not api_key:
        current_app.logger.error("RESEND_API_KEY no configurada")
        print("⚠️ Resend no configurado - Email no enviado")
        return False
    
    # Configurar API key
    resend.api_key = api_key
    
    # Obtener email del remitente
    from_email = current_app.config.get('RESEND_FROM_EMAIL', 'onboarding@resend.dev')
    from_name = current_app.config.get('CLINICA_NOMBRE', 'Clínica Dental')
    
    try:
        params = {
            "from": f"{from_name} <{from_email}>",
            "to": [to] if isinstance(to, str) else to,
            "subject": subject,
            "html": html_content,
        }
        
        response = resend.Emails.send(params)
        current_app.logger.info(f"Correo enviado exitosamente a {to}")
        print(f"✅ Email enviado con Resend a {to}")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Error enviando correo con Resend: {str(e)}")
        print(f"⚠️ Error al enviar email con Resend: {e}")
        return False
