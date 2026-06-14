# Sistema de Gestión Odontológica

Aplicación web completa para la gestión integral de consultorios odontológicos con sistema de agentes autónomos.

## 🌟 Características

- **Gestión de Pacientes**: Registro completo de pacientes con historias clínicas
- **Sistema de Citas**: Programación y seguimiento de citas
- **Odontograma Digital**: Registro visual del estado dental
- **Portal del Paciente**: Acceso web para que los pacientes consulten su información
- **Sistema de Autenticación**: Control de acceso seguro para personal y pacientes
- **Notificaciones por Email**: Confirmaciones y recordatorios automáticos
- **🤖 Sistema de Agentes Autónomos**: 6 agentes que automatizan tareas sin intervención humana
  - 🔔 Recordatorios automáticos de citas (diario 9 AM)
  - 📋 Seguimiento de notas clínicas (2x día)
  - 🗑️ Limpieza de datos obsoletos (diario 2 AM)
  - 💾 Respaldos automáticos diarios (3 AM)
  - 📊 Reportes estadísticos (diario 8 AM)
  - 💌 Reactivación de pacientes inactivos (Lunes 10 AM)

## 🚀 Deploy en Internet

Este proyecto está listo para desplegar en **Render.com** (gratis):

👉 **Lee la guía completa**: [GUIA_RENDER.md](GUIA_RENDER.md)

### Deploy rápido:
1. Sube tu código a GitHub
2. Conecta con Render.com
3. Configura variables de entorno
4. ¡Listo! Accesible desde cualquier dispositivo

## 🐳 Docker

Incluye soporte completo para Docker:

```bash
# Desarrollo local con Docker
docker-compose up

# O construir manualmente
docker build -t sistema-odontologia .
docker run -p 5000:5000 --env-file .env sistema-odontologia
```

## 💻 Instalación Local

### Requisitos

- Python 3.10+
- pip

### Pasos

1. Clona el repositorio
2. Crea entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configura archivo `.env` (ver abajo)
5. Ejecuta:
   ```bash
   python run.py
   ```
   O usa `iniciar.bat` en Windows

## ⚙️ Configuración

Crea archivo `.env` con:

```env
SECRET_KEY=tu_clave_secreta_larga
FERNET_KEY=tu_fernet_key

# Email (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicación
CLINICA_EMAIL=admin@clinica.com
CLINICA_NOMBRE=Tu Clínica Dental

# URL base
BASE_URL=http://localhost:5000
```

**Para producción en Render:**
- `BASE_URL` debe ser tu URL de Render (ej: `https://tu-app.onrender.com`)
- Agrega `DATABASE_URL` para PostgreSQL

Ver [CONFIGURACION_EMAILS.md](CONFIGURACION_EMAILS.md) para detalles de email.

## 📁 Estructura del Proyecto

```
app/
├── auth/          # Autenticación y autorización
├── pacientes/     # Gestión de pacientes
├── citas/         # Sistema de citas
├── portal/        # Portal del paciente
├── public/        # Páginas públicas
├── main/          # Rutas principales y dashboard
├── static/        # CSS, JS, imágenes
├── templates/     # Plantillas HTML (Jinja2)
├── models.py      # Modelos de base de datos
├── agentes.py     # 🤖 Sistema de agentes autónomos
└── forms.py       # Formularios WTForms

planificador_agentes.py  # Scheduler (APScheduler)
config.py               # Configuración
run.py                  # Punto de entrada
```

## 🤖 Sistema de Agentes Autónomos

Los agentes operan 24/7 de forma independiente:

| Agente | Frecuencia | Función |
|--------|-----------|---------|
| 🔔 Recordatorios | Diario 9 AM | Envía recordatorios 24h antes de citas |
| 📋 Seguimiento | 2x día (9 AM, 9 PM) | Detecta citas sin notas clínicas |
| 🗑️ Limpieza | Diario 2 AM | Elimina datos obsoletos |
| 💾 Respaldo | Diario 3 AM | Crea backups automáticos |
| 📊 Reportes | Diario 8 AM | Envía estadísticas diarias |
| 💌 Reactivación | Lunes 10 AM | Contacta pacientes inactivos (6+ meses) |

Panel de control: `/dashboard/agentes` (requiere login como odontólogo)

Ver [SISTEMA_AGENTES.md](SISTEMA_AGENTES.md) para documentación completa.

## 📱 Acceso Multi-dispositivo

La aplicación es **Progressive Web App (PWA)** y funciona en:
- ✅ PC/Laptop (cualquier navegador)
- ✅ Móviles (responsive, instalable como app)
- ✅ Tablets
- ✅ Todos los sistemas operativos

En móvil, puedes **"Instalar aplicación"** para experiencia nativa.

## 🗄️ Base de Datos

- **Local**: SQLite (automático)
- **Producción (Render)**: PostgreSQL (recomendado)

El código detecta automáticamente el entorno y usa la BD correcta.

## 📚 Documentación

- [GUIA_RENDER.md](GUIA_RENDER.md) - Despliegue en internet paso a paso
- [SISTEMA_AGENTES.md](SISTEMA_AGENTES.md) - Documentación completa de agentes
- [CONFIGURACION_EMAILS.md](CONFIGURACION_EMAILS.md) - Configurar Gmail
- [GUIA_DEPLOYMENT_INTERNET.md](GUIA_DEPLOYMENT_INTERNET.md) - Alternativas de hosting

## 🔐 Seguridad

- Autenticación con Flask-Login
- Contraseñas hasheadas con bcrypt
- Protección CSRF en formularios
- Datos sensibles encriptados (Fernet)
- Variables de entorno para secretos

## 🛠️ Tecnologías

- **Backend**: Flask 3.0, SQLAlchemy
- **Frontend**: Bootstrap 5, JavaScript
- **Base de datos**: SQLite (local) / PostgreSQL (producción)
- **Agentes**: APScheduler 3.10
- **Email**: Flask-Mail (SMTP)
- **Servidor**: Gunicorn (producción)
- **Containerización**: Docker (opcional)

## 📝 Uso

1. Accede en `http://localhost:5000` (o tu URL de Render)
2. Inicia sesión como administrador
3. Registra pacientes y gestiona citas
4. Los pacientes acceden a `/portal` con sus credenciales
5. Los agentes trabajan automáticamente en segundo plano
6. Monitorea agentes en `/dashboard/agentes`

## 🎯 Próximos Pasos

1. **Desplegar en Render** - Sigue [GUIA_RENDER.md](GUIA_RENDER.md)
2. **Configurar PostgreSQL** - Para persistencia en producción
3. **Dominio personalizado** - Opcional, $10-15/año
4. **Certificado SSL** - Incluido gratis en Render

## 💰 Costos

- **Desarrollo local**: Gratis
- **Render Free**: Gratis (con limitaciones)
- **Render Producción**: $7-14/mes (sin sleep, BD más grande)

## 🤝 Contribuir

Este es un proyecto privado. Para reportar bugs o sugerir mejoras, contacta al administrador.

## 📄 Licencia

Todos los derechos reservados © 2026

---

**Desarrollado con ❤️ para clínicas odontológicas modernas**

🚀 **¿Listo para desplegar?** → Lee [GUIA_RENDER.md](GUIA_RENDER.md)
