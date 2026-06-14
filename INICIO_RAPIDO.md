# 🚀 Inicio Rápido - Sistema de Agentes

## Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
Edita el archivo `.env` y configura:
```env
SECRET_KEY=tu_clave_secreta
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicación
CLINICA_EMAIL=admin@clinica.com
CLINICA_NOMBRE=Clínica Dental
BASE_URL=http://localhost:5000
```

### 3. Iniciar la aplicación
```bash
python run.py
```

O en Windows:
```bash
iniciar.bat
```

## ¿Qué sucede al iniciar?

1. **Flask inicia** en `http://localhost:5000`
2. **Sistema de Agentes se activa automáticamente**
3. Verás en consola:
```
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

Próximas ejecuciones:
  • Agente de Recordatorios: 14/06/2026 11:00:00
  • Agente de Seguimiento: 14/06/2026 12:00:00
  ...
```

## Acceder al Panel de Agentes

1. Abre `http://localhost:5000`
2. Inicia sesión como **admin** (usuario: `admin`, contraseña: `admin123`)
3. Ve a **Agentes** en el menú superior
4. Verás el panel con todos los agentes y su estado

## Probar el Sistema

### Prueba Manual (sin esperar horarios)
```bash
python test_agentes.py
```

Esto ejecutará todos los agentes inmediatamente para verificar que funcionan.

### Ejecutar Agente Individual desde el Panel
1. Ve a `/dashboard/agentes`
2. Click en "Ejecutar Ahora" en cualquier agente
3. El agente se ejecutará inmediatamente

## Verificar que Funciona

### Logs en Consola
Los agentes imprimen mensajes cuando se ejecutan:
```
[AGENTE RECORDATORIOS] Ejecutando a las 2026-06-14 11:00:00
[AGENTE RECORDATORIOS] ✅ 3 recordatorios enviados
```

### Emails Enviados
Si configuraste correctamente el servidor de correo, verás emails en:
- Email del administrador (reportes, alertas)
- Email de pacientes (recordatorios, confirmaciones)

### Backups Creados
Revisa la carpeta `instance/backups/` para ver los respaldos automáticos:
```
instance/
  backups/
    odontologia_backup_20260614_030000.db
    odontologia_backup_20260613_030000.db
    ...
```

## Credenciales por Defecto

- **Usuario**: admin
- **Contraseña**: admin123
- **Rol**: odontologo (acceso completo)

## Estructura de Directorios

```
agente odontologia/
├── app/
│   ├── agentes.py              # ⭐ Definición de agentes
│   ├── templates/
│   │   └── agentes.html        # ⭐ Panel de control
│   └── ...
├── planificador_agentes.py     # ⭐ Scheduler
├── run.py                      # ⭐ Inicia app + agentes
├── test_agentes.py             # ⭐ Prueba de agentes
├── SISTEMA_AGENTES.md          # 📚 Documentación completa
├── requirements.txt
├── .env
└── instance/
    ├── odontologia.db
    └── backups/                # Carpeta de respaldos

⭐ = Archivos del sistema de agentes
```

## Solución de Problemas

### Los agentes no se ejecutan
- ✅ Verifica que APScheduler esté instalado: `pip install APScheduler==3.10.4`
- ✅ Revisa los logs en la consola
- ✅ Asegúrate de que la app esté corriendo

### No llegan emails
- ✅ Verifica configuración en `.env`
- ✅ Si usas Gmail, necesitas contraseña de aplicación (no tu contraseña normal)
- ✅ Consulta `CONFIGURACION_EMAILS.md`

### Error al crear backup
- ✅ Asegúrate de que la carpeta `instance/` existe
- ✅ Verifica permisos de escritura

## Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar aplicación
python run.py

# Probar agentes manualmente
python test_agentes.py

# Ver logs en tiempo real (si usas logging)
# Los agentes imprimen directamente en consola
```

## Próximos Pasos

1. ✅ Configurar emails correctamente
2. ✅ Cambiar contraseña del admin
3. ✅ Agregar pacientes de prueba
4. ✅ Crear citas de prueba
5. ✅ Ir a `/dashboard/agentes` y explorar
6. ✅ Ejecutar `test_agentes.py` para ver los agentes en acción
7. ✅ Revisar `SISTEMA_AGENTES.md` para documentación completa

## ¡Listo! 🎉

Tu sistema de gestión odontológica con agentes autónomos está funcionando.

Los agentes trabajan 24/7 sin intervención humana, automatizando:
- ✅ Recordatorios de citas
- ✅ Seguimiento de historiales
- ✅ Limpieza de datos
- ✅ Respaldos de seguridad
- ✅ Reportes estadísticos
- ✅ Reactivación de pacientes

**¿Necesitas ayuda?** Consulta `SISTEMA_AGENTES.md` o revisa los logs en consola.
