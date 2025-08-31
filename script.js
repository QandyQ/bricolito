function ajustarEscalaPuzzle() {
    const maxW = window.innerWidth * 0.95;
    const maxH = window.innerHeight * 0.85;
    const scale = Math.min(maxW / 1716, maxH / 895, 1);
    document.getElementById('puzzle-container').style.setProperty('--puzzle-scale', scale);
}
window.addEventListener('resize', ajustarEscalaPuzzle);
window.addEventListener('DOMContentLoaded', ajustarEscalaPuzzle);
const rows = 5, cols = 6, total = rows * cols;
const pieceWidth = 286, pieceHeight = 179;
const container = document.getElementById('puzzle-container');
let pieces = [];

// Crear piezas con posiciones correctas
for (let i = 0; i < total; i++) {
  const piece = document.createElement('div');
  piece.className = 'piece';
  const row = Math.floor(i / cols);
  const col = i % cols;
  piece.style.backgroundPosition = `-${col * pieceWidth}px -${row * pieceHeight}px`;
  piece.dataset.correct = i;
  pieces.push(piece);
}

// Mezclar piezas
pieces = pieces.sort(() => Math.random() - 0.5);

// Añadir piezas al contenedor
pieces.forEach(piece => container.appendChild(piece));

// Drag & Drop
let dragSrc = null;
container.addEventListener('dragstart', e => {
  if (e.target.classList.contains('piece')) {
    dragSrc = e.target;
    e.target.classList.add('dragging');
  }
});
container.addEventListener('dragend', e => {
  if (e.target.classList.contains('piece')) {
    e.target.classList.remove('dragging');
  }
});
container.addEventListener('dragover', e => e.preventDefault());
container.addEventListener('drop', e => {
  if (e.target.classList.contains('piece') && dragSrc && dragSrc !== e.target) {
    // Intercambiar piezas
    const srcIndex = Array.from(container.children).indexOf(dragSrc);
    const tgtIndex = Array.from(container.children).indexOf(e.target);
    if (srcIndex > -1 && tgtIndex > -1) {
      container.insertBefore(dragSrc, container.children[tgtIndex]);
      container.insertBefore(e.target, container.children[srcIndex]);
    }
    // Verificar si está resuelto
    let correcto = true;
    Array.from(container.children).forEach((p, idx) => {
      if (parseInt(p.dataset.correct) !== idx) correcto = false;
    });
    if (correcto) alert('¡Felicidades! Rompecabezas resuelto 🎉');
  }
});

// Hacer piezas arrastrables
document.querySelectorAll('.piece').forEach(p => p.setAttribute('draggable', 'true'));

// ...tu código anterior...

// Mostrar notificación de carta nueva
const notificacion = document.getElementById('notificacion-carta');
const btnIrUltima = document.getElementById('ir-ultima-carta');
if (cartas.length > 1) {
  notificacion.style.display = 'block';
  btnIrUltima.onclick = () => {
    actual = cartas.length - 1;
    mostrarCarta(actual);
    notificacion.style.display = 'none';
  };
  // Oculta la notificación automáticamente después de 10 segundos
  setTimeout(() => {
    notificacion.style.display = 'none';
  }, 10000);
}