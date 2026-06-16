"""
Sistema de Agentes Autónomos
Agentes que operan de forma independiente sin intervención humana
"""
from datetime import datetime, timedelta, date
from app import db
from app.models import Cita, Paciente, Usuario, CitaPublica, NotaClinica
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
        """Log de recordatorio (sin envío de email)"""
        clinica_nombre = current_app.config.get('CLINICA_NOMBRE', 'Clínica Dental')
        current_app.logger.info(f"[RECORDATORIO] Cita mañana: {cita.paciente.nombre} - {cita.fecha_hora.strftime('%d/%m/%Y %H:%M')} - {clinica_nombre}")
        print(f"📧 Recordatorio para: {cita.paciente.nombre} - {cita.fecha_hora.strftime('%d/%m/%Y %H:%M')}")
        return True  # Simular éxito


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
        """Log de alerta (sin envío de email)"""
        # Agrupar por odontólogo
        por_odontologo = {}
        for cita in citas:
            odontologo = cita.usuario.username
            if odontologo not in por_odontologo:
                por_odontologo[odontologo] = []
            por_odontologo[odontologo].append(cita)
        
        # Log de detalles
        for odontologo, lista_citas in por_odontologo.items():
            current_app.logger.warning(f"[SEGUIMIENTO] {odontologo} tiene {len(lista_citas)} citas sin notas clínicas")
            for cita in lista_citas:
                print(f"  - {cita.paciente.nombre} ({cita.fecha_hora.strftime('%d/%m/%Y')})")
        
        return True  # Simular éxito


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
        """Log de reporte (sin envío de email)"""
        clinica_nombre = current_app.config.get('CLINICA_NOMBRE', 'Clínica Dental')
        
        mensaje = f"""
[REPORTE DIARIO] {clinica_nombre} - {datos['fecha'].strftime('%d/%m/%Y')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Citas de hoy: {datos['citas_hoy']} (Completadas: {datos['citas_completadas']})
Pendientes de aprobación: {datos['citas_pendientes']}
Solicitudes web: {datos['solicitudes_publicas']}
Nuevos pacientes: {datos['pacientes_nuevos']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        current_app.logger.info(mensaje)
        print(mensaje)
        return True  # Simular éxito


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
        """Log de reactivación (sin envío de email)"""
        clinica_nombre = current_app.config.get('CLINICA_NOMBRE', 'Clínica Dental')
        current_app.logger.info(f"[REACTIVACION] Paciente inactivo: {paciente.nombre} - {clinica_nombre}")
        print(f"💌 Reactivación para: {paciente.nombre}")
        return True  # Simular éxito


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
