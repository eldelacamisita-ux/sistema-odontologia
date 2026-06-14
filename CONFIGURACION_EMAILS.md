# Configuración del Sistema de Notificaciones por Email

## 🎯 Funcionalidades Implementadas

### 1. Solicitud Pública de Cita (Sin Registro)
- ✅ Cliente llena formulario en página pública
- ✅ Email automático al odontólogo/recepcionista con los datos
- ✅ Formulario corregido y funcionando

### 2. Solicitud de Paciente Registrado
- ✅ Paciente registrado solicita cita desde su portal
- ✅ Email automático al odontólogo/recepcionista

### 3. Aprobación de Cita
- ✅ Admin aprueba cita
- ✅ Email automático de confirmación al paciente

### 4. Rechazo de Cita
- ✅ Admin rechaza cita con motivo
- ✅ Email automático al paciente explicando el motivo

---

## 📧 Configuración Requerida

### Paso 1: Instalar Flask-Mail

```bash
pip install Flask-Mail
```

O si ya actualizaste `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Paso 2: Configurar Gmail (Recomendado)

Para usar Gmail, necesitas generar una **Contraseña de Aplicación** (App Password):

1. **Habilitar verificación en 2 pasos**:
   - Ve a https://myaccount.google.com/security
   - Activa "Verificación en 2 pasos"

2. **Generar Contraseña de Aplicación**:
   - Ve a https://myaccount.google.com/apppasswords
   - Selecciona "Correo" y "Windows Computer" (o "Otro")
   - Clic en "Generar"
   - **Copia la contraseña de 16 caracteres**

### Paso 3: Configurar Variables de Entorno

Edita el archivo `.env` y completa con tus datos:

```env
# Configuración de Email (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx  # ← App Password de 16 caracteres
MAIL_DEFAULT_SENDER=tu-email@gmail.com
CLINICA_EMAIL=tu-email@gmail.com  # Email donde recibirás las notificaciones
CLINICA_NOMBRE=Clínica Dental
```

**Ejemplo Real:**
```env
MAIL_USERNAME=clinicadental2024@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop
MAIL_DEFAULT_SENDER=clinicadental2024@gmail.com
CLINICA_EMAIL=clinicadental2024@gmail.com
CLINICA_NOMBRE=Clínica Dental Sonrisas
```

### Paso 4: Alternativa - Otros Proveedores de Email

#### **Outlook/Hotmail**
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@outlook.com
MAIL_PASSWORD=tu-contraseña
```

#### **Yahoo**
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@yahoo.com
MAIL_PASSWORD=tu-app-password
```

#### **Servidor SMTP Personalizado**
```env
MAIL_SERVER=mail.tudominio.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=info@tudominio.com
MAIL_PASSWORD=tu-contraseña
```

---

## 🧪 Probar el Sistema

### Prueba 1: Solicitud Pública (Sin Registro)

1. **Abrir página pública:**
   ```
   http://localhost:5000
   ```

2. **Scroll hasta "Agenda tu Cita"**

3. **Llenar formulario:**
   - Nombre: Juan Pérez
   - Teléfono: +58 414 123-4567
   - Email: juan@example.com (opcional pero recomendado)
   - Fecha: Cualquier fecha futura
   - Motivo: Consulta de urgencia

4. **Clic "Enviar Solicitud"**

5. **Resultado:**
   - ✅ Mensaje de confirmación en pantalla
   - ✅ Email enviado a `CLINICA_EMAIL` con los datos
   - ✅ Solicitud guardada en base de datos

### Prueba 2: Solicitud de Paciente Registrado

1. **Login como paciente:**
   ```
   URL: http://localhost:5000/portal
   Usuario: paciente
   Contraseña: paciente123
   ```

2. **Ir a "Nueva Cita"**

3. **Llenar formulario:**
   - Fecha: Cualquier fecha futura
   - Hora: 10:00
   - Motivo: Revisión general

4. **Clic "Solicitar Cita"**

5. **Resultado:**
   - ✅ Cita guardada con estado "Pendiente"
   - ✅ Email enviado a `CLINICA_EMAIL`
   - ✅ Visible en "Mis Citas" como "Pendiente"

### Prueba 3: Aprobación de Cita

1. **Login como admin:**
   ```
   URL: http://localhost:5000/dashboard
   Usuario: admin
   Contraseña: admin123
   ```

2. **Clic en tarjeta "Pendientes"**

3. **Clic botón "✅ Aprobar" en una solicitud**

4. **Resultado:**
   - ✅ Estado cambia a "Programada"
   - ✅ **Email enviado al paciente confirmando la cita** ⭐
   - ✅ Paciente ve cita como "Confirmada"

### Prueba 4: Rechazo de Cita

1. **Como admin, en solicitudes pendientes**

2. **Clic botón "❌ Rechazar"**

3. **Seleccionar motivo:** "Día completo"

4. **Confirmar**

5. **Resultado:**
   - ✅ Estado cambia a "Rechazada"
   - ✅ **Email enviado al paciente explicando el motivo** ⭐
   - ✅ Paciente ve cita como "Rechazada"

---

## 📧 Ejemplos de Emails

### Email 1: Notificación de Solicitud Pública (Admin)
```
Asunto: 📅 Nueva Solicitud de Cita - Juan Pérez

Nueva solicitud de cita recibida:

Paciente: Juan Pérez
Teléfono: +58 414 123-4567
Email: juan@example.com
Fecha preferida: 25/06/2026
Mensaje: Consulta de urgencia

Fecha de solicitud: 14/06/2026 15:30

[Ver en Panel de Administración]
```

### Email 2: Notificación de Solicitud de Paciente (Admin)
```
Asunto: 📅 Nueva Solicitud de Cita - Juan Pérez (Prueba)

⏰ Estado: PENDIENTE DE APROBACIÓN

Nueva solicitud de cita de paciente registrado:

Paciente: Juan Pérez (Prueba)
Teléfono: +58 414 123-4567
Email: paciente@test.com
Fecha solicitada: 21/06/2026 10:00
Motivo: Revisión general

[Ver Solicitudes Pendientes]
```

### Email 3: Confirmación de Cita (Paciente)
```
Asunto: ✅ Cita Confirmada - Clínica Dental

¡Hola Juan Pérez!

Tu cita ha sido CONFIRMADA:

📅 Fecha: 21/06/2026
🕐 Hora: 10:00
🏥 Lugar: Clínica Dental
💬 Motivo: Revisión general

⚠️ Importante: Por favor, llega 10 minutos antes de tu cita.

[Ver Mis Citas]

¡Te esperamos!
Clínica Dental
```

### Email 4: Rechazo de Cita (Paciente)
```
Asunto: ❌ Solicitud de Cita - Clínica Dental

Hola Juan Pérez,

Lamentablemente no podemos confirmar tu cita para:

📅 Fecha solicitada: 21/06/2026
🕐 Hora solicitada: 10:00

Motivo: Día completo (5 citas ya confirmadas)

Por favor, contáctanos para encontrar otra fecha disponible.

Clínica Dental
```

---

## ⚠️ Solución de Problemas

### Problema 1: Emails no se envían

**Verificar:**
1. ✅ Flask-Mail instalado: `pip list | grep Flask-Mail`
2. ✅ Variables en `.env` correctamente configuradas
3. ✅ App Password de Gmail generada correctamente
4. ✅ Verificación en 2 pasos habilitada en Gmail

**Ver logs:**
```python
# Los errores aparecen en la consola del servidor
Error al enviar email: [SMTPAuthenticationError]...
```

**Soluciones comunes:**
- Verifica que el App Password no tenga espacios extras
- Asegúrate de usar el App Password, no tu contraseña normal
- Verifica que `MAIL_USE_TLS=True` esté configurado

### Problema 2: Email del paciente no recibe confirmación

**Causa:** Paciente no tiene email registrado

**Solución:**
1. Como admin, edita el paciente
2. Agrega un email válido
3. Intenta aprobar la cita nuevamente

### Problema 3: Emails van a spam

**Soluciones:**
- Usa un dominio propio en lugar de Gmail
- Configura SPF y DKIM en tu dominio
- Pide al paciente agregar el email a contactos

---

## 🔒 Seguridad

### Buenas Prácticas:

1. **Nunca subas `.env` a git:**
   - Ya está en `.gitignore`
   - Contiene credenciales sensibles

2. **Usa App Passwords:**
   - Más seguro que contraseña real
   - Puedes revocarlas sin afectar la cuenta

3. **En producción:**
   - Usa un servidor SMTP dedicado (SendGrid, Mailgun)
   - Configura límites de envío
   - Monitorea logs de emails

4. **Variables sensibles:**
   ```env
   # ❌ MAL - Contraseña real
   MAIL_PASSWORD=MiContraseña123
   
   # ✅ BIEN - App Password
   MAIL_PASSWORD=abcd efgh ijkl mnop
   ```

---

## 📊 Estadísticas de Emails

Para ver cuántos emails se han enviado, puedes agregar logging:

```python
# En app/email_utils.py, línea 13
print(f"✅ Email enviado: {subject} → {recipients}")
```

---

## 🎉 Estado Final

✅ **Sistema de Notificaciones Completo**

| Acción | Email Admin | Email Paciente |
|--------|-------------|----------------|
| Solicitud pública | ✅ Sí | ❌ No |
| Solicitud paciente | ✅ Sí | ❌ No |
| Aprobar cita | ❌ No | ✅ Sí |
| Rechazar cita | ❌ No | ✅ Sí |

---

## 💡 Mejoras Futuras

1. **Templates de Email Personalizados:**
   - Usar archivos HTML separados
   - Logo de la clínica
   - Colores personalizados

2. **Recordatorios Automáticos:**
   - Email 24h antes de la cita
   - Email 1 hora antes de la cita
   - Usar Celery para tareas programadas

3. **Confirmación de Lectura:**
   - Saber si el paciente abrió el email
   - Usar servicios como SendGrid

4. **SMS además de Email:**
   - Usar Twilio para SMS
   - Más efectivo que email

5. **WhatsApp:**
   - API de WhatsApp Business
   - Mayor tasa de apertura

---

## 📞 Soporte

Si tienes problemas configurando Gmail:
- https://support.google.com/accounts/answer/185833
- https://support.google.com/mail/answer/7126229

Para otros proveedores de email:
- Consulta la documentación SMTP de tu proveedor
- Busca "SMTP settings" + nombre del proveedor

---

¡Sistema de notificaciones completamente funcional! 🎊
