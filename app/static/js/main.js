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