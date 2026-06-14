# 🤖 Sistema de Agentes Autónomos

## ¿Qué es un Agente?

Un **agente** es un programa que opera de forma **autónoma** (sin intervención humana constante) y tiene tres capacidades principales:

1. **PERCEPCIÓN**: Observa y analiza el entorno (base de datos, archivos, etc.)
2. **DECISIÓN**: Evalúa la información según reglas predefinidas
3. **ACCIÓN**: Ejecuta tareas automáticamente

## Agentes Implementados

### 1. 🔔 Agente de Recordatorios
**Frecuencia**: Cada hora

**Función**: Envía recordatorios automáticos a pacientes 24 horas antes de su cita.

**Operación**:
- **Percepción**: Consulta la base de datos buscando citas programadas para mañana
- **Decisión**: Identifica pacientes con email registrado
- **Acción**: Envía emails de recordatorio automáticamente sin intervención humana

**Beneficio**: Reduce ausencias y mejora la organización

---

### 2. 📋 Agente de Seguimiento
**Frecuencia**: Cada 6 horas (00:00, 06:00, 12:00, 18:00)

**Función**: Detecta citas completadas sin notas clínicas y alerta al personal médico.

**Operación**:
- **Percepción**: Busca citas con estado "completada" en los últimos 7 días
- **Decisión**: Verifica si existe nota clínica asociada
- **Acción**: Envía alerta al odontólogo responsable si falta documentación

**Beneficio**: Asegura completitud de historiales médicos

---

### 3. 🗑️ Agente de Limpieza
**Frecuencia**: Diario a las 2:00 AM

**Función**: Elimina datos obsoletos para mantener el sistema optimizado.

**Operación**:
- **Percepción**: Identifica citas canceladas de más de 90 días y solicitudes atendidas de más de 30 días
- **Decisión**: Determina qué registros ya no son necesarios
- **Acción**: Elimina automáticamente de la base de datos

**Beneficio**: Mantiene la base de datos limpia y rápida

---

### 4. 💾 Agente de Respaldo
**Frecuencia**: Diario a las 3:00 AM

**Función**: Crea respaldos automáticos de la base de datos.

**Operación**:
- **Percepción**: Detecta la ubicación de la base de datos activa
- **Decisión**: Genera nombre con timestamp único
- **Acción**: 
  - Crea copia de seguridad en carpeta `/instance/backups/`
  - Elimina respaldos más antiguos de 7 días

**Beneficio**: Protección contra pérdida de datos

---

### 5. 📊 Agente de Reportes
**Frecuencia**: Diario a las 8:00 AM

**Función**: Genera y envía reportes estadísticos al administrador.

**Operación**:
- **Percepción**: Recopila estadísticas del día anterior
  - Citas realizadas
  - Citas pendientes
  - Nuevos pacientes
  - Solicitudes web sin atender
- **Decisión**: Formatea información en reporte legible
- **Acción**: Envía email al administrador con el reporte HTML

**Beneficio**: Visibilidad del estado del negocio sin esfuerzo manual

---

### 6. 💌 Agente de Reactivación
**Frecuencia**: Lunes y Jueves a las 10:00 AM

**Función**: Detecta pacientes inactivos y envía mensajes de reactivación.

**Operación**:
- **Percepción**: Busca pacientes sin citas en los últimos 6 meses
- **Decisión**: Filtra aquellos con email registrado
- **Acción**: Envía email amigable invitándolos a agendar nueva cita (máximo 10 por ejecución)

**Beneficio**: Recupera pacientes inactivos y aumenta retención

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────┐
│      APLICACIÓN FLASK (run.py)          │
│                                          │
│  ┌────────────────────────────────┐    │
│  │  Planificador de Agentes       │    │
│  │  (APScheduler)                 │    │
│  │                                 │    │
│  │  ┌───────────────────────┐    │    │
│  │  │ AGENTE 1: Recordatorios│    │    │
│  │  │ Trigger: Cada hora     │    │    │
│  │  └───────────────────────┘    │    │
│  │                                 │    │
│  │  ┌───────────────────────┐    │    │
│  │  │ AGENTE 2: Seguimiento  │    │    │
│  │  │ Trigger: Cada 6 horas  │    │    │
│  │  └───────────────────────┘    │    │
│  │                                 │    │
│  │  ┌───────────────────────┐    │    │
│  │  │ AGENTE 3: Limpieza     │    │    │
│  │  │ Trigger: 2:00 AM       │    │    │
│  │  └───────────────────────┘    │    │
│  │                                 │    │
│  │  ┌───────────────────────┐    │    │
│  │  │ AGENTE 4: Respaldo     │    │    │
│  │  │ Trigger: 3:00 AM       │    │    │
│  │  └───────────────────────┘    │    │
│  │                                 │    │
│  │  ┌───────────────────────┐    │    │
│  │  │ AGENTE 5: Reportes     │    │    │
│  │  │ Trigger: 8:00 AM       │    │    │
│  │  └───────────────────────┘    │    │
│  │                                 │    │
│  │  ┌───────────────────────┐    │    │
│  │  │ AGENTE 6: Reactivación │    │    │
│  │  │ Trigger: Lun/Jue 10 AM │    │    │
│  │  └───────────────────────┘    │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │    Base de Datos SQLite        │    │
│  │    Sistema de Emails           │    │
│  │    Sistema de Archivos         │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

## Archivos del Sistema

```
/app/
  agentes.py                  # Definición de todos los agentes
planificador_agentes.py       # Scheduler que ejecuta agentes
run.py                        # Aplicación principal (inicia agentes)
/app/templates/
  agentes.html               # Panel de control de agentes
/instance/
  backups/                   # Carpeta de respaldos automáticos
```

## Uso del Panel de Control

### Acceder al Panel
1. Iniciar sesión como **odontólogo**
2. Ir a **Agentes** en el menú superior
3. Ver estado de todos los agentes

### Ejecutar Agente Manualmente
1. En el panel de agentes, cada tarjeta tiene un botón "Ejecutar Ahora"
2. Click en el botón del agente deseado
3. El agente se ejecutará inmediatamente (fuera de su horario normal)

### Monitorear Ejecuciones
- Cada agente muestra su próxima ejecución programada
- Los logs de ejecución aparecen en la consola del servidor
- Los emails enviados quedan registrados

## Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Iniciar la aplicación
```bash
python run.py
```

Los agentes se iniciarán automáticamente al arrancar la aplicación.

### 3. Verificar funcionamiento
```
Verás en la consola:
============================================================
✅ SISTEMA DE AGENTES AUTÓNOMOS INICIADO
============================================================

Programación de agentes:
  🔔 Recordatorios:    Cada hora
  📋 Seguimiento:      Cada 6 horas
  🗑️  Limpieza:         Diario 2:00 AM
  💾 Respaldo:         Diario 3:00 AM
  📊 Reportes:         Diario 8:00 AM
  💌 Reactivación:     Lunes y Jueves 10:00 AM

============================================================
```

## Configuración de Emails

Para que los agentes funcionen correctamente, asegúrate de configurar el servidor de emails en `.env`:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicación
CLINICA_EMAIL=admin@clinica.com
CLINICA_NOMBRE=Clínica Dental
BASE_URL=http://localhost:5000
```

Ver `CONFIGURACION_EMAILS.md` para más detalles.

## Ventajas del Sistema

✅ **Automatización total**: Los agentes trabajan 24/7 sin intervención humana
✅ **Reducción de carga laboral**: El personal se enfoca en tareas importantes
✅ **Mejora la experiencia del paciente**: Recordatorios y reactivaciones automáticas
✅ **Protección de datos**: Respaldos automáticos diarios
✅ **Visibilidad**: Reportes automáticos del estado del negocio
✅ **Calidad**: Asegura que las historias clínicas estén completas
✅ **Optimización**: Limpieza automática mantiene el sistema eficiente

## Diferencia: Agente vs Aplicación Web

### Aplicación Web Tradicional
- Usuario hace click → Sistema responde
- Reactivo (responde a acciones)
- Requiere intervención humana constante

### Sistema de Agentes
- Sistema observa → Sistema decide → Sistema actúa
- Proactivo (actúa por sí mismo)
- Opera autónomamente sin intervención

## ¿Necesitas IA?

**NO**. Los agentes implementados usan:
- Lógica programada (if-else)
- Consultas a base de datos
- Reglas de negocio predefinidas
- Programación temporal (cron)

**No hay inteligencia artificial** en este sistema. Son agentes autónomos basados en reglas.

## Mantenimiento

### Agregar un Nuevo Agente

1. **Crear la clase en `app/agentes.py`**:
```python
class AgenteNuevo:
    @staticmethod
    def ejecutar():
        # PERCEPCIÓN
        datos = consultar_base_datos()
        
        # DECISIÓN
        if condicion:
            # ACCIÓN
            realizar_tarea()
```

2. **Programar en `planificador_agentes.py`**:
```python
self.scheduler.add_job(
    func=self._ejecutar_con_contexto(AgenteNuevo.ejecutar),
    trigger=CronTrigger(hour=9, minute=0),
    id='agente_nuevo',
    name='Agente Nuevo'
)
```

3. **Agregar tarjeta en `templates/agentes.html`**

## Soporte

Para dudas o problemas con el sistema de agentes, revisar:
1. Logs en la consola del servidor
2. Panel de control en `/dashboard/agentes`
3. Configuración de emails en `.env`
4. Este documento

---

**Sistema desarrollado**: Junio 2026
**Versión**: 1.0
**Tecnología**: Flask + APScheduler
