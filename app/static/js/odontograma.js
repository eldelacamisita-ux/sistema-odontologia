let dientesData = {};
let estadosMap = {};

function initOdontograma(initialData, estados) {
    dientesData = initialData || {};
    estadosMap = estados;
    // Aplicar colores visuales iniciales
    document.querySelectorAll('.diente-card').forEach(card => {
        const diente = card.dataset.diente;
        const estado = dientesData[diente] || 'sano';
        actualizarCardVisual(card, estado);
        card.addEventListener('click', () => abrirSelector(diente, card));
    });
}

function actualizarCardVisual(card, estado) {
    const estadoInfo = estadosMap[estado];
    if(estadoInfo) {
        card.style.backgroundColor = estado === 'sano' ? '#d4edda' :
                                   (estado === 'caries' ? '#f8d7da' :
                                   (estado === 'tratado' ? '#fff3cd' : '#e2e3e5'));
        card.querySelector('.estado-icono').innerHTML = estadoInfo.icono;
        card.querySelector('.estado-texto').innerHTML = estadoInfo.texto;
    }
}

let dienteSeleccionado = null;
let cardSeleccionada = null;

function abrirSelector(diente, card) {
    dienteSeleccionado = diente;
    cardSeleccionada = card;
    // Resaltar card
    document.querySelectorAll('.diente-card').forEach(c => c.style.border = '1px solid #ccc');
    card.style.border = '3px solid #0d6efd';
    // Mostrar mensaje o usar botones ya existentes
    const selectorBtns = document.querySelectorAll('.estado-selector');
    selectorBtns.forEach(btn => {
        btn.classList.remove('active');
        btn.addEventListener('click', () => {
            const nuevoEstado = btn.dataset.estado;
            dientesData[dienteSeleccionado] = nuevoEstado;
            actualizarCardVisual(cardSeleccionada, nuevoEstado);
            document.getElementById('dientes_json').value = JSON.stringify(dientesData);
            // Quitar resaltado
            cardSeleccionada.style.border = '1px solid #ccc';
            dienteSeleccionado = null;
        });
    });
}