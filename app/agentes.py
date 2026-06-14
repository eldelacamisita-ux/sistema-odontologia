"""
Sistema de Agentes Autónomos
Agentes que operan de forma independiente sin intervención humana
"""
from datetime import datetime, timedelta, date
from app import db
from app.models import Cita, Paciente, Usuario, CitaPublica, NotaClinica
from app.email_utils import send_email
from flask import current_app
import shutil
import os

class AgenteRecordatorios:
    """
    Agente que envía recordatorios automáticos de citas
    Se ejecuta cada hora y envía recordatorios 24h antes
    """
    
    @staticmethod
    def ejecutar():
        """Percibe el entorno y actúa autónomamente"""
        print(f"[AGENTE RECORDATORIOS] Ejecutando a las {datetime.now()}")
        
        # PERCEPCIÓN: Detectar citas que necesitan recordatorio
        manana = datetime.now() + timedelta(days=1)
        inicio_ventana = manana.replace(hour=0, minute=0, second=0)
        fin_ventana = manana.replace(hour=23, minute=59, second=59)
        
        citas = Cita.query.filter(
            Cita.fecha_hora >= inicio_ventana,
            Cita.fecha_hora <= fin_ventana,
            Cita.estado == 'programada'
        ).all()
        
        # ACCIÓN: Enviar recordatorios automáticamente
        enviados = 0
        for cita in citas:
            if cita.paciente.email:
                exito = AgenteRecordatorios._enviar_recordatorio(cita)
                if exito:
                    enviados += 1
        
        print(f"[AGENTE RECORDATORIOS] ✅ {enviados} recordatorios enviados")
        return {"enviados": enviados, "total": len(citas)}
    
    @staticmethod
    def _enviar_recordatorio(cita):
        """Enviar recordatorio al paciente"""
        clinica_nombre = current_app.config.get('CLINICA_NOMBRE', 'Clínica Dental')
        
        subject = f"🔔 Recordatorio de Cita - {clinica_nombre}"
        
        text_body = f"""
¡Hola {cita.paciente.nombre}!

Este es un recordatorio de tu cita MAÑANA:

📅 Fecha: {cita.fecha_hora.strftime('%d/%m/%Y')}
🕐 Hora: {cita.fecha_hora.strftime('%H:%M')}
🏥 Lugar: {clinica_nombre}
💬 Motivo: {cita.motivo or 'Consulta general'}

⚠️ Por favor, llega 10 minutos antes.

Si no puedes asistir, contáctanos con anticipación.

¡Te esperamos!
{clinica_nombre}
        """
        
        html_body = f"""
<html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; border: 2px solid #ffc107; border-radius: 8px; padding: 20px;">
            <div style="text-align: center; background-color: #ffc107; color: black; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                <h2 style="margin: 0;">🔔 Recordatorio de Cita</h2>
            </div>
            
            <p>¡Hola <strong>{cita.paciente.nombre}</strong>!</p>
            
            <p>Este es un recordatorio de tu cita <strong>MAÑANA</strong>:</p>
            
            <div style="background-color: #fff3cd; padding: 20px; border-radius: 4px; margin: 20px 0; border-left: 4px solid #ffc107;">
                <p style="margin: 5px 0; font-size: 16px;"><strong>📅 Fecha:</strong> {cita.fecha_hora.strftime('%d/%m/%Y')}</p>
                <p style="margin: 5px 0; font-size: 16px;"><strong>🕐 Hora:</strong> {cita.fecha_hora.strftime('%H:%M')}</p>
                <p style="margin: 5px 0;"><strong>🏥 Lugar:</strong> {clinica_nombre}</p>
                <p style="margin: 5px 0;"><strong>💬 Motivo:</strong> {cita.motivo or 'Consulta general'}</p>
            </div>
            
            <div style="background-color: #f8d7da; padding: 15px; border-radius: 4px; margin: 20px 0;">
                <p style="margin: 0;"><strong>⚠️ Importante:</strong> Por favor, llega 10 minutos antes de tu cita.</p>
            </div>
            
            <p>Si no puedes asistir, contáctanos con anticipación.</p>
            
            <hr>
            
            <p style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
                ¡Te esperamos!<br>
                <strong>{clinica_nombre}</strong>
            </p>
        </div>
    </body>
</html>
        """
        
        return send_email(subject, cita.paciente.email, text_body, html_body)


class AgenteSeguimiento:
    """
    Agente que detecta citas completadas sin notas clínicas
    Envía alertas al personal médico
    """
    
    @staticmethod
    def ejecutar():
        """Detectar citas sin seguimiento y alertar"""
        print(f"[AGENTE SEGUIMIENTO] Ejecutando a las {datetime.now()}")
        
        # PERCEPCIÓN: Buscar citas completadas sin notas
        hace_7_dias = datetime.now() - timedelta(days=7)
        
        citas_sin_notas = Cita.query.filter(
            Cita.estado == 'completada',
            Cita.fecha_hora >= hace_7_dias
        ).all()
        
        # Filtrar las que no tienen notas clínicas
        citas_alerta = []
        for cita in citas_sin_notas:
            notas = NotaClinica.query.filter_by(paciente_id=cita.paciente_id).filter(
                NotaClinica.fecha >= cita.fecha_hora
            ).first()
            if not notas:
                citas_alerta.append(cita)
        
        # ACCIÓN: Enviar alertas al personal
        if citas_alerta:
            AgenteSeguimiento._enviar_alerta(citas_alerta)
        
        print(f"[AGENTE SEGUIMIENTO] ⚠️ {len(citas_alerta)} citas requieren seguimiento")
        return {"citas_sin_notas": len(citas_alerta)}
    
    @staticmethod
    def _enviar_alerta(citas):
        """Enviar alerta al personal médico"""
        clinica_email = current_app.config.get('CLINICA_EMAIL')
        
        # Agrupar por odontólogo
        por_odontologo = {}
        for cita in citas:
            odontologo = cita.usuario.username
            if odontologo not in por_odontologo:
                por_odontologo[odontologo] = []
            por_odontologo[odontologo].append(cita)
        
        # Construir mensaje
        detalles = ""
        for odontologo, lista_citas in por_odontologo.items():
            detalles += f"\n{odontologo}:\n"
            for cita in lista_citas:
                detalles += f"  - {cita.paciente.nombre} ({cita.fecha_hora.strftime('%d/%m/%Y')})\n"
        
        subject = f"⚠️ Citas sin Notas Clínicas - Seguimiento Requerido"
        
        text_body = f"""
ALERTA AUTOMÁTICA - SEGUIMIENTO DE CITAS

Se detectaron {len(citas)} citas completadas sin notas clínicas en los últimos 7 días:

{detalles}

Por favor, registra las notas clínicas correspondientes.

Este es un mensaje automático del Sistema de Agentes.
        """
        
        return send_email(subject, clinica_email, text_body)


class AgenteLimpieza:
    """
    Agente que limpia datos obsoletos
    Elimina citas canceladas antiguas y solicitudes atendidas
    """
    
    @staticmethod
    def ejecutar():
        """Limpiar datos obsoletos del sistema"""
        print(f"[AGENTE LIMPIEZA] Ejecutando a las {datetime.now()}")
        
        # PERCEPCIÓN: Detectar datos antiguos
        hace_90_dias = datetime.now() - timedelta(days=90)
        
        # ACCIÓN 1: Eliminar citas canceladas antiguas
        citas_canceladas = Cita.query.filter(
            Cita.estado == 'cancelada',
            Cita.fecha_hora < hace_90_dias
        ).all()
        
        eliminadas_citas = len(citas_canceladas)
        for cita in citas_canceladas:
            db.session.delete(cita)
        
        # ACCIÓN 2: Eliminar solicitudes públicas atendidas antiguas
        hace_30_dias = datetime.now() - timedelta(days=30)
        solicitudes_antiguas = CitaPublica.query.filter(
            CitaPublica.atendido == True,
            CitaPublica.fecha_solicitud < hace_30_dias
        ).all()
        
        eliminadas_solicitudes = len(solicitudes_antiguas)
        for solicitud in solicitudes_antiguas:
            db.session.delete(solicitud)
        
        db.session.commit()
        
        print(f"[AGENTE LIMPIEZA] 🗑️ Eliminadas {eliminadas_citas} citas y {eliminadas_solicitudes} solicitudes")
        return {
            "citas_eliminadas": eliminadas_citas,
            "solicitudes_eliminadas": eliminadas_solicitudes
        }


class AgenteRespaldo:
    """
    Agente que realiza respaldos automáticos de la base de datos
    """
    
    @staticmethod
    def ejecutar():
        """Crear respaldo de la base de datos"""
        print(f"[AGENTE RESPALDO] Ejecutando a las {datetime.now()}")
        
        try:
            # PERCEPCIÓN: Ubicar archivo de BD
            db_path = os.path.join(
                current_app.instance_path,
                'odontologia.db'
            )
            
            # ACCIÓN: Crear respaldo con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = os.path.join(current_app.instance_path, 'backups')
            
            # Crear directorio si no existe
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_path = os.path.join(
                backup_dir,
                f'odontologia_backup_{timestamp}.db'
            )
            
            shutil.copy2(db_path, backup_path)
            
            # Limpiar respaldos antiguos (mantener solo últimos 7 días)
            AgenteRespaldo._limpiar_respaldos_antiguos(backup_dir)
            
            print(f"[AGENTE RESPALDO] 💾 Respaldo creado: {backup_path}")
            return {"backup_creado": backup_path}
            
        except Exception as e:
            print(f"[AGENTE RESPALDO] ❌ Error: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def _limpiar_respaldos_antiguos(backup_dir):
        """Eliminar respaldos más antiguos de 7 días"""
        hace_7_dias = datetime.now() - timedelta(days=7)
        
        for filename in os.listdir(backup_dir):
            if filename.startswith('odontologia_backup_') and filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if file_time < hace_7_dias:
                    os.remove(filepath)
                    print(f"[AGENTE RESPALDO] 🗑️ Eliminado respaldo antiguo: {filename}")


class AgenteReportes:
    """
    Agente que genera reportes automáticos diarios
    """
    
    @staticmethod
    def ejecutar():
        """Generar y enviar reporte diario"""
        print(f"[AGENTE REPORTES] Ejecutando a las {datetime.now()}")
        
        # PERCEPCIÓN: Recopilar estadísticas
        hoy = date.today()
        inicio_dia = datetime.combine(hoy, datetime.min.time())
        fin_dia = datetime.combine(hoy, datetime.max.time())
        
        citas_hoy = Cita.query.filter(
            Cita.fecha_hora >= inicio_dia,
            Cita.fecha_hora <= fin_dia
        ).count()
        
        citas_completadas = Cita.query.filter(
            Cita.fecha_hora >= inicio_dia,
            Cita.fecha_hora <= fin_dia,
            Cita.estado == 'completada'
        ).count()
        
        citas_pendientes = Cita.query.filter(
            Cita.estado == 'pendiente'
        ).count()
        
        solicitudes_publicas = CitaPublica.query.filter(
            CitaPublica.atendido == False
        ).count()
        
        pacientes_nuevos = Paciente.query.filter(
            Paciente.fecha_registro >= inicio_dia
        ).count()
        
        # ACCIÓN: Enviar reporte
        AgenteReportes._enviar_reporte({
            'fecha': hoy,
            'citas_hoy': citas_hoy,
            'citas_completadas': citas_completadas,
            'citas_pendientes': citas_pendientes,
            'solicitudes_publicas': solicitudes_publicas,
            'pacientes_nuevos': pacientes_nuevos
        })
        
        print(f"[AGENTE REPORTES] 📊 Reporte diario generado")
        return {
            "citas_hoy": citas_hoy,
            "citas_completadas": citas_completadas
        }
    
    @staticmethod
    def _enviar_reporte(datos):
        """Enviar reporte por email"""
        clinica_email = current_app.config.get('CLINICA_EMAIL')
        clinica_nombre = current_app.config.get('CLINICA_NOMBRE', 'Clínica Dental')
        
        subject = f"📊 Reporte Diario - {datos['fecha'].strftime('%d/%m/%Y')}"
        
        text_body = f"""
REPORTE DIARIO AUTOMÁTICO
{clinica_nombre}
Fecha: {datos['fecha'].strftime('%d/%m/%Y')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CITAS DE HOY:
• Total: {datos['citas_hoy']}
• Completadas: {datos['citas_completadas']}

PENDIENTES DE ATENCIÓN:
• Citas por aprobar: {datos['citas_pendientes']}
• Solicitudes web: {datos['solicitudes_publicas']}

NUEVOS PACIENTES:
• Registrados hoy: {datos['pacientes_nuevos']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Este es un reporte automático generado por el Sistema de Agentes.
        """
        
        html_body = f"""
<html>
    <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
        <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="text-align: center; background-color: #0066cc; color: white; padding: 20px; border-radius: 4px; margin-bottom: 20px;">
                <h1 style="margin: 0;">📊 Reporte Diario</h1>
                <p style="margin: 5px 0 0 0;">{clinica_nombre}</p>
                <p style="margin: 5px 0 0 0; font-size: 14px;">{datos['fecha'].strftime('%d/%m/%Y')}</p>
            </div>
            
            <div style="margin: 20px 0;">
                <h3 style="color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 5px;">📅 Citas de Hoy</h3>
                <table style="width: 100%; margin: 10px 0;">
                    <tr>
                        <td style="padding: 8px; background-color: #f8f9fa;">Total programadas:</td>
                        <td style="padding: 8px; background-color: #f8f9fa; text-align: right;"><strong>{datos['citas_hoy']}</strong></td>
                    </tr>
                    <tr>
                        <td style="padding: 8px;">Completadas:</td>
                        <td style="padding: 8px; text-align: right;"><strong style="color: #28a745;">{datos['citas_completadas']}</strong></td>
                    </tr>
                </table>
            </div>
            
            <div style="margin: 20px 0;">
                <h3 style="color: #ffc107; border-bottom: 2px solid #ffc107; padding-bottom: 5px;">⏳ Pendientes de Atención</h3>
                <table style="width: 100%; margin: 10px 0;">
                    <tr>
                        <td style="padding: 8px; background-color: #fff3cd;">Citas por aprobar:</td>
                        <td style="padding: 8px; background-color: #fff3cd; text-align: right;"><strong>{datos['citas_pendientes']}</strong></td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; background-color: #f8f9fa;">Solicitudes web:</td>
                        <td style="padding: 8px; background-color: #f8f9fa; text-align: right;"><strong>{datos['solicitudes_publicas']}</strong></td>
                    </tr>
                </table>
            </div>
            
            <div style="margin: 20px 0;">
                <h3 style="color: #28a745; border-bottom: 2px solid #28a745; padding-bottom: 5px;">👥 Nuevos Pacientes</h3>
                <table style="width: 100%; margin: 10px 0;">
                    <tr>
                        <td style="padding: 8px; background-color: #d4edda;">Registrados hoy:</td>
                        <td style="padding: 8px; background-color: #d4edda; text-align: right;"><strong>{datos['pacientes_nuevos']}</strong></td>
                    </tr>
                </table>
            </div>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
            
            <p style="text-align: center; color: #666; font-size: 12px;">
                Reporte automático generado por el Sistema de Agentes<br>
                {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            </p>
        </div>
    </body>
</html>
        """
        
        return send_email(subject, clinica_email, text_body, html_body)


class AgenteReactivacion:
    """
    Agente que detecta pacientes inactivos y sugiere reactivación
    """
    
    @staticmethod
    def ejecutar():
        """Detectar pacientes inactivos y enviar sugerencias"""
        print(f"[AGENTE REACTIVACION] Ejecutando a las {datetime.now()}")
        
        # PERCEPCIÓN: Buscar pacientes sin citas en 6 meses
        hace_6_meses = datetime.now() - timedelta(days=180)
        
        # Todos los pacientes
        todos_pacientes = Paciente.query.all()
        
        pacientes_inactivos = []
        for paciente in todos_pacientes:
            # Buscar última cita
            ultima_cita = Cita.query.filter_by(paciente_id=paciente.id).order_by(
                Cita.fecha_hora.desc()
            ).first()
            
            if not ultima_cita or ultima_cita.fecha_hora < hace_6_meses:
                if paciente.email:  # Solo si tiene email
                    pacientes_inactivos.append(paciente)
        
        # ACCIÓN: Enviar emails de reactivación
        enviados = 0
        for paciente in pacientes_inactivos[:10]:  # Máximo 10 por ejecución
            exito = AgenteReactivacion._enviar_reactivacion(paciente)
            if exito:
                enviados += 1
        
        print(f"[AGENTE REACTIVACION] 💌 {enviados} emails de reactivación enviados")
        return {
            "pacientes_inactivos": len(pacientes_inactivos),
            "emails_enviados": enviados
        }
    
    @staticmethod
    def _enviar_reactivacion(paciente):
        """Enviar email de reactivación"""
        clinica_nombre = current_app.config.get('CLINICA_NOMBRE', 'Clínica Dental')
        base_url = current_app.config.get('BASE_URL', 'http://localhost:5000')
        
        subject = f"¡Te extrañamos! 😊 - {clinica_nombre}"
        
        text_body = f"""
¡Hola {paciente.nombre}!

Hace tiempo que no sabemos de ti. En {clinica_nombre} nos gustaría saber cómo estás.

Tu salud dental es importante para nosotros. ¿Cuándo fue tu última revisión?

Te recordamos que se recomienda una visita al dentista cada 6 meses.

¿Te gustaría agendar una cita? Es muy fácil:
{base_url}/portal

¡Esperamos verte pronto!

{clinica_nombre}
        """
        
        html_body = f"""
<html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; border: 2px solid #0066cc; border-radius: 8px; padding: 20px;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #0066cc; margin: 0;">😊 ¡Te extrañamos!</h2>
            </div>
            
            <p>¡Hola <strong>{paciente.nombre}</strong>!</p>
            
            <p>Hace tiempo que no sabemos de ti. En <strong>{clinica_nombre}</strong> nos gustaría saber cómo estás.</p>
            
            <div style="background-color: #e7f3ff; padding: 20px; border-radius: 4px; margin: 20px 0; border-left: 4px solid #0066cc;">
                <p style="margin: 0;">🦷 Tu salud dental es importante para nosotros.</p>
                <p style="margin: 10px 0 0 0;">¿Cuándo fue tu última revisión?</p>
            </div>
            
            <p>Te recordamos que se recomienda una visita al dentista cada <strong>6 meses</strong>.</p>
            
            <p style="text-align: center; margin: 30px 0;">
                <a href="{base_url}/portal" style="background-color: #0066cc; color: white; padding: 15px 30px; text-decoration: none; border-radius: 4px; font-size: 16px;">
                    Agendar una Cita
                </a>
            </p>
            
            <p>¡Esperamos verte pronto!</p>
            
            <hr>
            
            <p style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
                <strong>{clinica_nombre}</strong><br>
                Tu salud dental, nuestra prioridad
            </p>
        </div>
    </body>
</html>
        """
        
        return send_email(subject, paciente.email, text_body, html_body)


# Coordinador de Agentes
class CoordinadorAgentes:
    """
    Coordina la ejecución de todos los agentes
    """
    
    @staticmethod
    def ejecutar_todos():
        """Ejecutar todos los agentes en secuencia"""
        print(f"\n{'='*60}")
        print(f"INICIANDO SISTEMA DE AGENTES AUTÓNOMOS")
        print(f"Hora: {datetime.now()}")
        print(f"{'='*60}\n")
        
        resultados = {}
        
        try:
            resultados['recordatorios'] = AgenteRecordatorios.ejecutar()
        except Exception as e:
            print(f"[ERROR] Agente Recordatorios: {e}")
            resultados['recordatorios'] = {"error": str(e)}
        
        try:
            resultados['seguimiento'] = AgenteSeguimiento.ejecutar()
        except Exception as e:
            print(f"[ERROR] Agente Seguimiento: {e}")
            resultados['seguimiento'] = {"error": str(e)}
        
        try:
            resultados['limpieza'] = AgenteLimpieza.ejecutar()
        except Exception as e:
            print(f"[ERROR] Agente Limpieza: {e}")
            resultados['limpieza'] = {"error": str(e)}
        
        try:
            resultados['respaldo'] = AgenteRespaldo.ejecutar()
        except Exception as e:
            print(f"[ERROR] Agente Respaldo: {e}")
            resultados['respaldo'] = {"error": str(e)}
        
        try:
            resultados['reportes'] = AgenteReportes.ejecutar()
        except Exception as e:
            print(f"[ERROR] Agente Reportes: {e}")
            resultados['reportes'] = {"error": str(e)}
        
        try:
            resultados['reactivacion'] = AgenteReactivacion.ejecutar()
        except Exception as e:
            print(f"[ERROR] Agente Reactivación: {e}")
            resultados['reactivacion'] = {"error": str(e)}
        
        print(f"\n{'='*60}")
        print(f"SISTEMA DE AGENTES COMPLETADO")
        print(f"{'='*60}\n")
        
        return resultados
