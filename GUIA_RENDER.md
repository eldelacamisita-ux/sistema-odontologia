# 🚀 Guía de Despliegue en Render.com

## ✅ Preparación Completada

Tu proyecto ya está limpio y optimizado con:
- ✅ Archivos innecesarios eliminados
- ✅ Dependencias limpiadas (PyQt5 y PyInstaller eliminados)
- ✅ Gunicorn agregado para producción
- ✅ Dockerfile creado
- ✅ render.yaml configurado
- ✅ docker-compose.yml para desarrollo local

---

## 📋 Paso 1: Preparar Repositorio Git

### Si NO tienes Git inicializado:

```bash
git init
git add .
git commit -m "Sistema de Gestión Odontológica con Agentes Autónomos"
```

### Crear repositorio en GitHub:

1. Ve a https://github.com/new
2. Nombre: `sistema-odontologia` (o el que prefieras)
3. **NO inicialices con README** (ya lo tienes)
4. Crear repositorio

### Subir código a GitHub:

```bash
git remote add origin https://github.com/TU_USUARIO/sistema-odontologia.git
git branch -M main
git push -u origin main
```

---

## 🌐 Paso 2: Desplegar en Render.com

### 2.1 Crear Cuenta

1. Ve a https://render.com
2. Click en **"Get Started for Free"**
3. **Sign up with GitHub** (recomendado)
4. Autoriza Render para acceder a tus repositorios

### 2.2 Crear Web Service

1. En el dashboard de Render, click **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub:
   - Click en **"Connect"** junto a tu repositorio `sistema-odontologia`
4. Configurar el servicio:
   - **Name**: `sistema-odontologia` (o el que prefieras)
   - **Region**: Oregon (US West) - más cercano a Latinoamérica
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 run:app`
   - **Plan**: **Free** ⭐

5. Click en **"Advanced"** para configurar variables de entorno

### 2.3 Configurar Variables de Entorno

En la sección **"Environment Variables"**, agrega:

```
SECRET_KEY = [genera una clave aleatoria larga]
FERNET_KEY = 6KjW6PxK2BdLkf6jW5jX5jW5jX5jW5jX5jW5jX5jW5=
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = eldelacamisita@gmail.com
MAIL_PASSWORD = fehb fypi bnud zxyq
MAIL_DEFAULT_SENDER = eldelacamisita@gmail.com
CLINICA_EMAIL = eldelacamisita@gmail.com
CLINICA_NOMBRE = Clínica Dental
BASE_URL = https://sistema-odontologia.onrender.com
```

**⚠️ IMPORTANTE**: Reemplaza `BASE_URL` con tu URL real de Render (te la darán después del deploy)

### 2.4 Desplegar

1. Click en **"Create Web Service"**
2. Espera 5-10 minutos mientras Render:
   - ✅ Clona tu repositorio
   - ✅ Instala dependencias
   - ✅ Inicia tu aplicación

3. Verás logs en tiempo real:
```
==> Cloning from GitHub...
==> Running build command 'pip install -r requirements.txt'...
==> Starting service with 'gunicorn...'
✅ SISTEMA DE AGENTES AUTÓNOMOS INICIADO
```

### 2.5 Acceder a tu Aplicación

Tu URL será: `https://sistema-odontologia.onrender.com`

**Actualiza BASE_URL**:
1. Ve a "Environment" en Render
2. Edita `BASE_URL` con tu URL real
3. Guarda (se reiniciará automáticamente)

---

## 🤖 Verificar que los Agentes Funcionan

1. Accede a tu aplicación
2. Inicia sesión como odontólogo
3. Ve a **"Agentes"** en el menú
4. Deberías ver los 6 agentes con sus próximas ejecuciones

**Los agentes funcionan en Render Free** ✅ porque:
- APScheduler corre en el mismo proceso que Flask
- No son procesos separados (permitidos en Free)

---

## 📊 Limitaciones del Plan Gratuito de Render

### ⚠️ Lo que debes saber:

1. **Se duerme después de 15 minutos de inactividad**
   - Primera carga después de dormir: 30-60 segundos
   - Solución: Plan pagado ($7/mes) o mantener activo con pings

2. **750 horas gratis al mes**
   - Suficiente para: ~31 días si está activo 24/7
   - Si se duerme: ilimitado (no cuenta mientras duerme)

3. **Base de datos SQLite NO persiste** entre deploys
   - Render reinicia contenedores frecuentemente
   - **SOLUCIÓN**: Usar PostgreSQL (incluido gratis en Render)

---

## 💾 IMPORTANTE: Migrar de SQLite a PostgreSQL

### ¿Por qué?
- SQLite en Render se borra con cada deploy
- PostgreSQL es persistente y gratuito

### Cómo hacerlo:

#### 1. Crear Base de Datos PostgreSQL en Render

1. En Render, click **"New +"**
2. Selecciona **"PostgreSQL"**
3. Name: `odontologia-db`
4. Plan: **Free** (100 MB, suficiente para empezar)
5. Click **"Create Database"**
6. Copia la **"Internal Database URL"**

#### 2. Actualizar Código

Edita `config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    FERNET_KEY = os.environ.get('FERNET_KEY', '')
    
    # Base de datos: PostgreSQL en producción, SQLite en local
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Render usa postgres://, SQLAlchemy necesita postgresql://
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///odontologia.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_USERNAME'))
    
    # Información de la clínica
    CLINICA_EMAIL = os.environ.get('CLINICA_EMAIL', 'admin@clinica.com')
    CLINICA_NOMBRE = os.environ.get('CLINICA_NOMBRE', 'Clínica Dental')
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
```

Agrega PostgreSQL a `requirements.txt`:

```
psycopg2-binary==2.9.9
```

#### 3. Configurar Variable en Render

En tu Web Service, ve a "Environment":
- Agrega variable: `DATABASE_URL`
- Valor: La "Internal Database URL" que copiaste

#### 4. Redeploy

1. Commit cambios:
```bash
git add .
git commit -m "Migrar a PostgreSQL"
git push
```

2. Render se redespliega automáticamente

---

## 🐳 Opción Alternativa: Docker

### ¿Docker vs Render directo?

#### ✅ Render Directo (Recomendado para ti)
- Más fácil, sin complejidad
- Deploy automático desde GitHub
- Gratis, perfecto para empezar

#### 🐳 Docker (Para desarrollo local o servidores propios)
- Bueno para: correr en tu PC, VPS propios, servidores empresariales
- Más complejo, necesitas conocimientos de Docker
- Render soporta Docker, pero no es necesario

### Si quieres usar Docker localmente:

```bash
# Construir imagen
docker build -t sistema-odontologia .

# Correr contenedor
docker run -p 5000:5000 --env-file .env sistema-odontologia
```

O con docker-compose:

```bash
docker-compose up
```

---

## 🔄 Actualizar la Aplicación

### Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción de cambios"
git push
```

**Render se actualiza automáticamente** 🎉

---

## 🐛 Solución de Problemas

### La aplicación no inicia

1. Revisa los logs en Render (tab "Logs")
2. Busca errores de Python
3. Verifica que todas las variables de entorno estén configuradas

### Los agentes no ejecutan

- **Normal en Free**: Si la app se duerme, los agentes también
- **Solución**: Plan pagado ($7/mes) o ping automático

### Error de Base de Datos

- Si usas SQLite: **Migra a PostgreSQL** (ver arriba)
- Los datos se pierden en cada deploy con SQLite

### Emails no se envían

1. Verifica configuración GMAIL en variables de entorno
2. Asegúrate de usar contraseña de aplicación, no tu contraseña normal
3. Revisa logs para mensajes de error

---

## 💰 Costos

### Plan Gratuito (Suficiente para empezar):
- ✅ Web Service: Gratis (con sleep)
- ✅ PostgreSQL: 100 MB gratis
- ✅ Dominio: `.onrender.com` gratis

### Si necesitas más adelante:
- **$7/mes**: Web service sin sleep, siempre activo
- **$7/mes**: PostgreSQL 1 GB (cuando crezcas)
- **Dominio propio**: $10-15/año (opcional)

**Total recomendado para producción seria: $14/mes**

---

## ✅ Checklist Final

Antes de desplegar, verifica:

- [ ] Código en GitHub
- [ ] Cuenta de Render creada
- [ ] Variables de entorno configuradas
- [ ] BASE_URL apunta a tu URL de Render
- [ ] PostgreSQL creado y conectado
- [ ] `psycopg2-binary` en requirements.txt
- [ ] config.py actualizado para PostgreSQL
- [ ] Git push realizado

---

## 🎉 ¡Listo!

Tu aplicación estará disponible en:
`https://tu-nombre.onrender.com`

**Características funcionando:**
- ✅ Gestión de pacientes y citas
- ✅ Portal del paciente
- ✅ Odontograma digital
- ✅ 6 agentes autónomos trabajando 24/7
- ✅ Emails automáticos
- ✅ Respaldos automáticos
- ✅ Accesible desde cualquier dispositivo

---

## 📞 Soporte

Si tienes problemas:
1. Revisa logs en Render
2. Consulta esta guía
3. Verifica configuración de variables de entorno

**¡Éxito con tu despliegue!** 🚀
