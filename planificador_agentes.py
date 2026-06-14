"""
Planificador de Agentes Autónomos
Ejecuta los agentes según una programación definida
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app import create_app
from app.agentes import (
    AgenteRecordatorios,
    AgenteSeguimiento,
    AgenteLimpieza,
    AgenteRespaldo,
    AgenteReportes,
    AgenteReactivacion
)
from datetime import datetime

class PlanificadorAgentes:
    """
    Planificador que ejecuta agentes de forma automática
    """
    
    def __init__(self, app):
        self.app = app
        self.scheduler = BackgroundScheduler()
        self._configurar_trabajos()
    
    def _configurar_trabajos(self):
        """Configurar la programación de cada agente"""
        
        # AGENTE RECORDATORIOS: Diario a las 9:00 AM (en vez de cada hora)
        self.scheduler.add_job(
            func=self._ejecutar_con_contexto(AgenteRecordatorios.ejecutar),
            trigger=CronTrigger(hour=9, minute=0),  # Solo una vez al día
            id='agente_recordatorios',
            name='Agente de Recordatorios',
            replace_existing=True
        )
        
        # AGENTE SEGUIMIENTO: Cada 12 horas (en vez de 6)
        self.scheduler.add_job(
            func=self._ejecutar_con_contexto(AgenteSeguimiento.ejecutar),
            trigger=CronTrigger(hour='9,21'),  # 9 AM y 9 PM
            id='agente_seguimiento',
            name='Agente de Seguimiento',
            replace_existing=True
        )
        
        # AGENTE LIMPIEZA: Diario a las 2 AM
        self.scheduler.add_job(
            func=self._ejecutar_con_contexto(AgenteLimpieza.ejecutar),
            trigger=CronTrigger(hour=2, minute=0),
            id='agente_limpieza',
            name='Agente de Limpieza',
            replace_existing=True
        )
        
        # AGENTE RESPALDO: Diario a las 3 AM
        self.scheduler.add_job(
            func=self._ejecutar_con_contexto(AgenteRespaldo.ejecutar),
            trigger=CronTrigger(hour=3, minute=0),
            id='agente_respaldo',
            name='Agente de Respaldo',
            replace_existing=True
        )
        
        # AGENTE REPORTES: Diario a las 8 AM
        self.scheduler.add_job(
            func=self._ejecutar_con_contexto(AgenteReportes.ejecutar),
            trigger=CronTrigger(hour=8, minute=0),
            id='agente_reportes',
            name='Agente de Reportes',
            replace_existing=True
        )
        
        # AGENTE REACTIVACIÓN: Solo Lunes a las 10 AM (en vez de Lunes y Jueves)
        self.scheduler.add_job(
            func=self._ejecutar_con_contexto(AgenteReactivacion.ejecutar),
            trigger=CronTrigger(day_of_week='mon', hour=10, minute=0),
            id='agente_reactivacion',
            name='Agente de Reactivación',
            replace_existing=True
        )
    
    def _ejecutar_con_contexto(self, func):
        """Wrapper para ejecutar función dentro del contexto de Flask"""
        def wrapper():
            with self.app.app_context():
                try:
                    return func()
                except Exception as e:
                    print(f"ERROR en agente: {e}")
                    import traceback
                    traceback.print_exc()
        return wrapper
    
    def iniciar(self):
        """Iniciar el planificador"""
        self.scheduler.start()
        print("\n" + "="*60)
        print("✅ SISTEMA DE AGENTES AUTÓNOMOS INICIADO")
        print("="*60)
        print("\nProgramación de agentes (Frecuencias reducidas para evitar spam):")
        print("  🔔 Recordatorios:    Diario 9:00 AM")
        print("  📋 Seguimiento:      2x día (9 AM y 9 PM)")
        print("  🗑️  Limpieza:         Diario 2:00 AM")
        print("  💾 Respaldo:         Diario 3:00 AM")
        print("  📊 Reportes:         Diario 8:00 AM")
        print("  💌 Reactivación:     Solo Lunes 10:00 AM")
        print("\n" + "="*60 + "\n")
        
        # Mostrar próximas ejecuciones
        jobs = self.scheduler.get_jobs()
        if jobs:
            print("Próximas ejecuciones:")
            for job in jobs:
                next_run = job.next_run_time
                print(f"  • {job.name}: {next_run.strftime('%d/%m/%Y %H:%M:%S')}")
            print("\n" + "="*60 + "\n")
    
    def detener(self):
        """Detener el planificador"""
        self.scheduler.shutdown()
        print("\n⏹️  Sistema de Agentes detenido\n")
    
    def listar_trabajos(self):
        """Listar todos los trabajos programados"""
        jobs = self.scheduler.get_jobs()
        return [
            {
                'id': job.id,
                'nombre': job.name,
                'proxima_ejecucion': job.next_run_time.strftime('%d/%m/%Y %H:%M:%S') if job.next_run_time else 'N/A'
            }
            for job in jobs
        ]
    
    def ejecutar_ahora(self, agente_id):
        """Ejecutar un agente manualmente de forma inmediata"""
        job = self.scheduler.get_job(agente_id)
        if job:
            job.modify(next_run_time=datetime.now())
            return True
        return False


# Inicializar planificador global
_planificador = None

def obtener_planificador():
    """Obtener instancia del planificador"""
    return _planificador

def iniciar_planificador(app):
    """Iniciar el planificador de agentes"""
    global _planificador
    if _planificador is None:
        _planificador = PlanificadorAgentes(app)
        _planificador.iniciar()
    return _planificador

def detener_planificador():
    """Detener el planificador de agentes"""
    global _planificador
    if _planificador is not None:
        _planificador.detener()
        _planificador = None
