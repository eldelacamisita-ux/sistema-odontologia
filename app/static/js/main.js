// Función general para confirmaciones
document.addEventListener('DOMContentLoaded', function() {
    const deleteLinks = document.querySelectorAll('.btn-danger');
    deleteLinks.forEach(link => {
        if(link.getAttribute('onclick')) return;
        link.addEventListener('click', function(e) {
            if(!confirm('¿Estás seguro de eliminar este registro?')) {
                e.preventDefault();
            }
        });
    });
});

// ==========================================
// 🔔 NOTIFICACIONES DEL NAVEGADOR
// ==========================================

/**
 * Solicitar permiso para mostrar notificaciones
 */
function solicitarPermisoNotificaciones() {
    if (!('Notification' in window)) {
        console.log('❌ Este navegador no soporta notificaciones');
        return;
    }

    if (Notification.permission === 'granted') {
        console.log('✅ Permiso de notificaciones ya concedido');
        return;
    }

    if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                console.log('✅ Permiso de notificaciones concedido');
                // Mostrar notificación de bienvenida
                mostrarNotificacion(
                    '¡Bienvenido a OdontoSeguro!',
                    'Recibirás recordatorios de tus citas aquí.',
                    '/static/icons/android-chrome-192x192.png'
                );
            } else {
                console.log('⚠️ Permiso de notificaciones denegado');
            }
        });
    }
}

/**
 * Mostrar una notificación del navegador
 * @param {string} titulo - Título de la notificación
 * @param {string} mensaje - Mensaje de la notificación
 * @param {string} icono - Ruta al ícono (opcional)
 */
function mostrarNotificacion(titulo, mensaje, icono = '/static/icons/android-chrome-192x192.png') {
    if (!('Notification' in window)) {
        console.log('❌ Este navegador no soporta notificaciones');
        return;
    }
    
    if (Notification.permission !== 'granted') {
        console.log('⚠️ No hay permiso para mostrar notificaciones');
        return;
    }

    try {
        const notificacion = new Notification(titulo, {
            body: mensaje,
            icon: icono,
            tag: 'odontoseguro', // Evita notificaciones duplicadas
            requireInteraction: false, // No requiere interacción para cerrarse
            badge: icono,
            vibrate: [200, 100, 200] // Vibración en móviles
        });

        // Al hacer clic en la notificación, enfocar la ventana
        notificacion.onclick = function() {
            window.focus();
            this.close();
        };

        // Cerrar automáticamente después de 10 segundos
        setTimeout(() => {
            notificacion.close();
        }, 10000);

        console.log('✅ Notificación mostrada:', titulo);
    } catch (error) {
        console.error('❌ Error mostrando notificación:', error);
    }
}

/**
 * Verificar si hay citas próximas desde el servidor
 */
function verificarCitasProximas() {
    fetch('/api/citas-proximas')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener citas próximas');
            }
            return response.json();
        })
        .then(data => {
            if (data.citas && data.citas.length > 0) {
                // Mostrar solo la primera cita (evitar spam de notificaciones)
                const cita = data.citas[0];
                mostrarNotificacion(
                    '📅 Recordatorio de cita',
                    `${cita.paciente} - ${cita.fecha} ${cita.hora}`,
                    '/static/icons/android-chrome-192x192.png'
                );
                
                console.log(`✅ ${data.citas.length} citas próximas encontradas`);
            } else {
                console.log('📭 No hay citas próximas en las próximas 24 horas');
            }
        })
        .catch(error => {
            console.error('❌ Error al verificar citas:', error);
        });
}

// ==========================================
// 🚀 INICIALIZACIÓN
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    // Solicitar permiso después de 3 segundos (no molestar inmediatamente)
    setTimeout(solicitarPermisoNotificaciones, 3000);
    
    // Verificar citas próximas al cargar la página (solo si está autenticado)
    if (document.body.classList.contains('authenticated')) {
        setTimeout(verificarCitasProximas, 5000);
    }
});

// Verificar cada 10 minutos si hay citas próximas (solo si está autenticado)
if (document.body.classList.contains('authenticated')) {
    setInterval(verificarCitasProximas, 600000); // 10 minutos
}

// ==========================================
// 🌐 EXPORTAR FUNCIONES GLOBALMENTE
// ==========================================

window.mostrarNotificacion = mostrarNotificacion;
window.solicitarPermisoNotificaciones = solicitarPermisoNotificaciones;
window.verificarCitasProximas = verificarCitasProximas;