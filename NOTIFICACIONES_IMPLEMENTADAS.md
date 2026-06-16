# 🔔 Notificaciones del Navegador - Implementadas

## ✅ ¿Qué se ha implementado?

### 1. Sistema de Notificaciones del Navegador (Web Notifications API)
- Solicitud de permisos al usuario
- Notificación de bienvenida al aprobar permisos
- Verificación automática de citas próximas cada 10 minutos
- Notificación automática al cargar el dashboard si hay citas próximas

### 2. API de Citas Próximas
- Endpoint: `/api/citas-proximas`
- Busca citas programadas en las próximas 24 horas
- Devuelve información del paciente, fecha, hora y motivo

### 3. Funciones JavaScript Disponibles

#### `solicitarPermisoNotificaciones()`
Solicita permiso al usuario para mostrar notificaciones.
- Se ejecuta automáticamente 3 segundos después de cargar la página
- Solo pide permiso si no ha sido concedido previamente

#### `mostrarNotificacion(titulo, mensaje, icono)`
Muestra una notificación del navegador.
```javascript
mostrarNotificacion(
    '📅 Recordatorio de cita',
    'Juan Pérez - 17/06/2026 10:00',
    '/static/icons/android-chrome-192x192.png'
);
```

#### `verificarCitasProximas()`
Consulta el servidor para verificar si hay citas en las próximas 24 horas.
- Se ejecuta automáticamente al cargar la página (después de 5 segundos)
- Se ejecuta cada 10 minutos automáticamente
- Muestra notificación solo de la primera cita (evita spam)

## 🎯 Flujo de Funcionamiento

### Al Cargar la Página:
1. **+3 segundos:** Se solicita permiso para notificaciones
2. **+5 segundos:** Se verifica si hay citas próximas (primera vez)
3. **Cada 10 minutos:** Se vuelve a verificar automáticamente

### Al Cargar el Dashboard:
- Si hay citas próximas (48h), muestra una notificación automática con el total

### Tipos de Notificaciones:

#### 1. Notificación de Bienvenida
```
Título: ¡Bienvenido a OdontoSeguro!
Mensaje: Recibirás recordatorios de tus citas aquí.
```

#### 2. Notificación de Citas Próximas (Dashboard)
```
Título: 📋 Recordatorio
Mensaje: Tienes X citas próximas en las próximas 48 horas.
```

#### 3. Notificación de Cita Individual (API)
```
Título: 📅 Recordatorio de cita
Mensaje: [Nombre Paciente] - [DD/MM/YYYY] [HH:MM]
```

## 📱 Compatibilidad

### ✅ Funciona en:
- Chrome (Windows, Mac, Linux, Android)
- Edge (Windows, Mac)
- Firefox (Windows, Mac, Linux, Android)
- Safari (Mac, iOS 16.4+) - Con limitaciones
- Opera (Windows, Mac, Linux, Android)

### ⚠️ Limitaciones:
- **iOS Safari:** Notificaciones solo funcionan en PWA instaladas (no en navegador)
- **Navegador cerrado:** Estas notificaciones NO funcionan con el navegador cerrado
- **Pestaña cerrada:** Solo funciona si al menos una pestaña de la app está abierta

### 🔥 Para notificaciones con navegador cerrado:
Se necesitaría implementar **Push Notifications con Firebase Cloud Messaging** (FCM), que es más complejo y requiere:
- Cuenta de Firebase
- Configuración de tokens
- Service Worker con push events
- Backend para enviar push desde el servidor

## 🧪 Cómo Probar

### 1. Probar Localmente:

```bash
python run.py
```

1. Abre http://localhost:5000
2. Inicia sesión
3. Después de 3 segundos, te pedirá permiso para notificaciones → **Acepta**
4. Verás una notificación de bienvenida
5. Navega al dashboard:
   - Si hay citas próximas (48h), verás una notificación
6. Espera 10 minutos → verás otra verificación automática

### 2. Probar en Producción (Render):

1. Sube el código a GitHub:
   ```bash
   git add .
   git commit -m "🔔 Agregar notificaciones del navegador"
   git push origin main
   ```

2. Espera el deploy (3-5 minutos)

3. Abre tu URL en Chrome (Android o PC):
   ```
   https://tu-app.onrender.com
   ```

4. Acepta los permisos de notificaciones

5. Navega por la app y verás notificaciones automáticas

### 3. Forzar Notificación Manual:

Abre la consola del navegador (F12) y ejecuta:

```javascript
// Solicitar permiso
solicitarPermisoNotificaciones();

// Mostrar notificación de prueba
mostrarNotificacion('Prueba', 'Esta es una notificación de prueba');

// Verificar citas próximas
verificarCitasProximas();
```

## 🔧 Personalización

### Cambiar el Intervalo de Verificación

En `app/static/js/main.js`, línea ~130:

```javascript
// Cambiar 600000 (10 minutos) por otro valor en milisegundos
setInterval(verificarCitasProximas, 600000);

// Ejemplos:
// 5 minutos: 300000
// 15 minutos: 900000
// 30 minutos: 1800000
```

### Cambiar el Rango de Horas para Citas Próximas

En `app/main/routes.py`, función `api_citas_proximas`:

```python
# Cambiar 24 por el número de horas deseado
limite = ahora + timedelta(hours=24)

# Ejemplos:
# 12 horas: hours=12
# 48 horas: hours=48
# 1 semana: days=7
```

### Cambiar el Ícono de las Notificaciones

En `app/static/js/main.js`, funciones `mostrarNotificacion`:

```javascript
// Cambiar la ruta del ícono
icono = '/static/icons/mi-icono-personalizado.png'
```

### Cambiar el Tiempo de Cierre Automático

En `app/static/js/main.js`, función `mostrarNotificacion`:

```javascript
// Cambiar 10000 (10 segundos) por otro valor en milisegundos
setTimeout(() => {
    notificacion.close();
}, 10000);

// Ejemplos:
// 5 segundos: 5000
// 15 segundos: 15000
// 30 segundos: 30000
```

## 🎨 Agregar Notificaciones Personalizadas

### En Cualquier Template:

```html
<button onclick="mostrarNotificacion('Título', 'Mensaje')">
    Mostrar notificación
</button>
```

### Desde JavaScript:

```javascript
// Notificación simple
mostrarNotificacion('✅ Éxito', 'Operación completada');

// Notificación con ícono personalizado
mostrarNotificacion(
    '❌ Error',
    'No se pudo completar la operación',
    '/static/icons/error.png'
);
```

### Desde Python (Flask):

En cualquier route, puedes pasar una variable al template:

```python
@main_bp.route('/mi-ruta')
def mi_ruta():
    mensaje_notificacion = "Tienes 3 mensajes nuevos"
    return render_template('mi_template.html', 
                         mensaje_notificacion=mensaje_notificacion)
```

Y en el template:

```html
{% if mensaje_notificacion %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            mostrarNotificacion('Notificación', '{{ mensaje_notificacion }}');
        }, 2000);
    });
</script>
{% endif %}
```

## 🐛 Troubleshooting

### "No aparecen las notificaciones"

**Causas:**
1. El usuario no dio permiso
2. El navegador no soporta notificaciones
3. Las notificaciones están bloqueadas a nivel del sistema

**Solución:**
1. Abre la consola (F12) y busca mensajes de error
2. Verifica que `Notification.permission` sea `'granted'`:
   ```javascript
   console.log(Notification.permission);
   ```
3. Si es `'denied'`, resetea los permisos:
   - Chrome: Click en el candado (🔒) → Configuración del sitio → Notificaciones → Permitir
   - Firefox: Click en el candado → Borrar permisos y recargar

### "Las notificaciones no se ven en iPhone"

**Causa:** Safari en iOS solo muestra notificaciones si la PWA está instalada.

**Solución:**
1. Instala la PWA: Safari → Compartir → Agregar a pantalla de inicio
2. Abre la app desde la pantalla de inicio (no desde Safari)
3. Acepta los permisos de notificaciones

### "La API /api/citas-proximas da error 404"

**Causa:** El código no se actualizó correctamente en el servidor.

**Solución:**
1. Verifica que el archivo `app/main/routes.py` tenga la función `api_citas_proximas`
2. Reinicia el servidor: `python run.py`
3. Limpia caché: Ctrl+Shift+R

### "Las notificaciones no se cierran automáticamente"

**Causa:** Algunos navegadores/sistemas operativos ignoran el cierre automático.

**Solución:** Es un comportamiento del sistema operativo, no es un error. El usuario puede cerrarlas manualmente.

## 📊 Estadísticas

### Archivos Modificados:
- ✅ `app/static/js/main.js` - Funciones de notificaciones
- ✅ `app/main/routes.py` - API de citas próximas
- ✅ `app/templates/base.html` - Clase authenticated y script de notificación
- ✅ `app/templates/index.html` - (Sin cambios, usa el código de base.html)

### Líneas de Código Agregadas:
- JavaScript: ~150 líneas
- Python: ~20 líneas
- HTML/Jinja: ~15 líneas

### Funcionalidades Agregadas:
- ✅ Solicitud de permisos
- ✅ Notificaciones de bienvenida
- ✅ Verificación automática cada 10 minutos
- ✅ API de citas próximas
- ✅ Notificación al cargar dashboard
- ✅ Funciones globales exportadas

## 🔮 Próximas Mejoras (Opcional)

### 1. Notificaciones Push con Firebase (Navegador cerrado)
- Requiere cuenta de Firebase
- Funciona incluso si el navegador está cerrado
- Más complejo de implementar

### 2. Notificaciones por Email
- Ya implementado en el código original
- Se puede activar configurando SMTP

### 3. Notificaciones por WhatsApp/SMS
- Requiere integración con Twilio o similar
- Costo adicional por mensaje

### 4. Notificaciones Programadas
- El agente autónomo puede programar notificaciones
- Recordatorios 1 hora antes de la cita
- Recordatorios el día anterior

## ✅ Checklist de Deployment

- [x] Código JavaScript agregado en `main.js`
- [x] API `/api/citas-proximas` creada en routes
- [x] Template `base.html` modificado
- [x] Documentación completa
- [ ] Subir a GitHub (`git push`)
- [ ] Verificar deploy en Render
- [ ] Probar notificaciones en producción
- [ ] Probar en diferentes dispositivos (PC, Android, iPhone)

## 🎉 Resultado Final

Ahora tu aplicación:
- ✅ Es una PWA instalable
- ✅ Muestra notificaciones del navegador
- ✅ Verifica citas automáticamente cada 10 minutos
- ✅ Notifica al usuario cuando hay citas próximas
- ✅ Funciona en todos los navegadores modernos
- ✅ Experiencia similar a una app nativa

---

**¿Listo para el deploy?** Ejecuta:

```bash
git add .
git commit -m "🔔 Agregar notificaciones del navegador y API de citas próximas"
git push origin main
```
