# 🚀 DEPLOYMENT A RENDER - FASES 2 Y 3

## Preparación Antes del Deploy

### ✅ Verificación Local

1. **Probar la aplicación localmente:**
   ```bash
   cd "c:\Users\Cesar\Desktop\agente odontologia"
   python run.py
   ```

2. **Verificar que funcionen:**
   - ✅ Horarios se muestran en dashboard
   - ✅ Puedes agregar/eliminar horarios
   - ✅ Puedes subir comprobantes
   - ✅ Puedes aprobar/rechazar comprobantes

3. **Verificar archivos importantes:**
   - `requirements.txt` sin Flask-Mail, resend, email-validator
   - `.gitignore` incluye carpeta comprobantes
   - Carpeta `app/static/comprobantes/` existe con `.gitkeep`

---

## 📤 Subir a GitHub

### Paso 1: Hacer Commit

```bash
cd "c:\Users\Cesar\Desktop\agente odontologia"

# Ver cambios
git status

# Agregar todos los cambios
git add .

# Commit (puedes usar el mensaje de COMMIT_MESSAGE.txt)
git commit -m "feat: Implementar horarios de doctores y comprobantes de pago (Fases 2 y 3)"

# Push
git push origin main
```

---

## 🔄 Deploy Automático en Render

### Render detectará los cambios automáticamente

1. **Ve a tu dashboard de Render:** https://dashboard.render.com
2. **Busca tu servicio** de la aplicación de odontología
3. **Render iniciará el deploy automáticamente** cuando detecte el push

### Proceso de Deploy

```
1. Detectando cambios en GitHub... ✅
2. Clonando repositorio... ✅
3. Instalando dependencias (requirements.txt)... ✅
4. Ejecutando build... ✅
5. Iniciando aplicación... ✅
6. Deploy completo ✅
```

**Tiempo estimado:** 2-5 minutos

---

## ⚙️ Configuración Adicional en Render

### Variables de Entorno (si no las tienes ya)

En Render → Tu servicio → Environment:

```bash
# Base de datos (ya debería estar configurada)
DATABASE_URL=postgresql://...

# Clave secreta
SECRET_KEY=tu-clave-secreta-aqui

# Clave de encriptación (para notas clínicas)
FERNET_KEY=tu-clave-fernet-aqui

# Nombre de la clínica
CLINICA_NOMBRE=Clínica Dental

# NO necesitas variables de email (ya eliminadas)
```

### ⚠️ IMPORTANTE: Carpeta de Comprobantes

Render usa un **sistema de archivos efímero**, lo que significa que los archivos subidos (comprobantes) **SE PERDERÁN** cuando el servicio se reinicie.

**Soluciones:**

#### Opción 1: Usar almacenamiento externo (RECOMENDADO)

**AWS S3 (Amazon):**
```bash
# Instalar boto3
pip install boto3

# Variables en Render:
AWS_ACCESS_KEY_ID=tu-key
AWS_SECRET_ACCESS_KEY=tu-secret
AWS_BUCKET_NAME=tu-bucket
```

**Cloudinary (más fácil, gratis hasta 25GB):**
```bash
# Instalar cloudinary
pip install cloudinary

# Variables en Render:
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

#### Opción 2: Base de datos (no recomendado para archivos grandes)
- Guardar los archivos como BLOB en PostgreSQL
- No requiere servicios externos
- Puede hacer la BD muy pesada

#### Opción 3: Render Disks (de pago)
- Render ofrece discos persistentes
- Cuesta $1/mes por 1GB
- Configuración simple

**Para empezar (sin cambios):**
- La funcionalidad funcionará perfectamente en LOCAL
- En PRODUCCIÓN, los comprobantes se perderán al reiniciar
- Podrás implementar almacenamiento externo más adelante

---

## 🧪 Verificación Post-Deploy

### 1. Acceder a la Aplicación

Tu URL de Render: `https://tu-app.onrender.com`

### 2. Verificar Tablas Nuevas

**Render debería crear automáticamente:**
- Tabla `horario_doctor`
- Tabla `comprobante_pago`

Si no se crean, ve a la consola de Render (Shell) y ejecuta:
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Tablas creadas")
```

### 3. Verificar Seed de Horarios

Los horarios iniciales deberían crearse automáticamente. Para verificar:

1. Login como admin
2. Ir a Dashboard
3. Deberías ver 4 horarios en el card de horarios

Si no aparecen, ejecutar en Shell de Render:
```python
from app import create_app, db
from app.models import HorarioDoctor
from datetime import time

app = create_app()
with app.app_context():
    if not HorarioDoctor.query.first():
        horarios = [
            HorarioDoctor(doctor="Dr. Nelson Rodriguez", dia_semana="Lunes", hora_inicio=time(12, 0), hora_fin=time(15, 0)),
            HorarioDoctor(doctor="Dr. Nelson Rodriguez", dia_semana="Miércoles", hora_inicio=time(12, 0), hora_fin=time(15, 0)),
            HorarioDoctor(doctor="Dra. Werllith Rangel", dia_semana="Martes", hora_inicio=time(8, 0), hora_fin=time(11, 0)),
            HorarioDoctor(doctor="Dra. Werllith Rangel", dia_semana="Jueves", hora_inicio=time(8, 0), hora_fin=time(11, 0)),
        ]
        db.session.add_all(horarios)
        db.session.commit()
        print("✅ Horarios creados")
```

### 4. Probar Funcionalidades

**Horarios:**
- ✅ Ver horarios en dashboard
- ✅ Agregar nuevo horario (como admin)
- ✅ Eliminar horario

**Comprobantes:**
- ✅ Crear una cita de prueba
- ✅ Cambiar estado a "realizada"
- ✅ Subir comprobante (5 o 10 $)
- ✅ Ver comprobante en "Pagos"
- ✅ Aprobar o rechazar comprobante

---

## 📋 Checklist de Deploy

- [ ] Commit y push a GitHub realizado
- [ ] Render inició deploy automáticamente
- [ ] Deploy completado sin errores
- [ ] Aplicación accesible en URL de Render
- [ ] Login funciona
- [ ] Tablas nuevas creadas
- [ ] Seed de horarios ejecutado
- [ ] Horarios visibles en dashboard
- [ ] Puedo agregar/eliminar horarios
- [ ] Puedo subir comprobante de pago
- [ ] Puedo aprobar/rechazar comprobantes
- [ ] No hay errores en logs de Render

---

## 🐛 Solución de Problemas

### Error: "relation 'horario_doctor' does not exist"
**Solución:** Las tablas no se crearon. Ejecutar en Shell de Render:
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
```

### Error: "No module named 'werkzeug.utils'"
**Solución:** Ya está en requirements.txt (Werkzeug==3.0.1)

### No aparecen horarios en dashboard
**Solución:** Ejecutar seed manual (ver arriba)

### Error al subir comprobante
**Causa:** Carpeta comprobantes no existe
**Solución:** La aplicación la crea automáticamente con `os.makedirs(UPLOAD_FOLDER, exist_ok=True)`

### Comprobantes desaparecen después de un tiempo
**Causa:** Render usa sistema de archivos efímero
**Solución:** Implementar almacenamiento externo (S3, Cloudinary) - ver arriba

---

## 📊 Monitoreo

### Logs en Render

Para ver logs en tiempo real:
1. Render Dashboard → Tu servicio → Logs
2. Verás todos los logs de la aplicación
3. Busca mensajes como:
   - `✅ Horarios iniciales creados`
   - `✅ Usuario admin creado`
   - Errores si los hay

### Métricas

Render muestra:
- CPU usage
- Memory usage
- Request rate
- Error rate

---

## 🎉 ¡Listo!

Si todo salió bien:

1. ✅ Aplicación desplegada en Render
2. ✅ Horarios funcionando
3. ✅ Comprobantes funcionando
4. ✅ Sin errores

**Próximo paso:** Implementar PWA cuando estés listo

---

## 📞 Contacto y Soporte

Si encuentras problemas:
1. Revisa los logs de Render
2. Verifica las variables de entorno
3. Confirma que las tablas se crearon
4. Prueba las funcionalidades localmente primero

---

**Última actualización:** 16/06/2026
**Estado:** ✅ LISTO PARA DEPLOY A RENDER
