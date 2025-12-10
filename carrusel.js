// Carrusel tipo slider
const track = document.querySelector('.carrusel-track');
const cartas = document.querySelectorAll('.carrusel-track .contenedor');
const indicador = document.getElementById('carrusel-indicador');
let actual = 0;

function mostrarCarta(idx) {
    cartas.forEach((c, i) => c.classList.toggle('carta-activa', i === idx));
    indicador.textContent = (idx + 1) + ' / ' + cartas.length;
    // Calcula el desplazamiento para centrar la carta activa
    const cartaWidth = cartas[0].offsetWidth + 40; // 40 = 2*margin
    const offset = (cartaWidth * idx) - ((track.offsetWidth - cartaWidth) / 2);
    track.style.transform = `translateX(${-offset}px)`;
}
document.getElementById('prev-carta').onclick = () => {
    actual = (actual - 1 + cartas.length) % cartas.length;
    mostrarCarta(actual);
};
document.getElementById('next-carta').onclick = () => {
    actual = (actual + 1) % cartas.length;
    mostrarCarta(actual);
};
mostrarCarta(actual);

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
  }, 20000);
}
// Bloquear acceso en móviles
if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    document.body.innerHTML = '<div style="text-align:center;padding:4em;font-size:1.5em;color:#c94f6d;">Esta página solo está disponible en computadoras.</div>';
    // Opcional: redirigir a otra página
    // window.location.href = "pagina_no_soportada.html";
}

// ==== IMÁGENES CAYENDO DESDE ARRIBA EN BUCLE ====
const fallingRoot = document.getElementById('falling-container');

// Lista de archivos en la carpeta "fotos" (ajusta los nombres reales)
const fotosLista = [
  'fotos/1.jpg','fotos/2.jpg','fotos/3.jpg','fotos/4.jpg','fotos/5.jpg',
  'fotos/6.jpg','fotos/7.jpg','fotos/8.jpg','fotos/9.jpg','fotos/10.jpg',
  'fotos/11.jpg','fotos/12.jpg','fotos/13.jpg','fotos/14.jpg','fotos/15.jpg',
  'fotos/16.jpg','fotos/17.jpg'
];

function crearFallingItem() {
  if (!fallingRoot || fotosLista.length === 0) return;

  const img = document.createElement('img');
  img.className = 'falling-item';

  // Elegir imagen aleatoria
  img.src = fotosLista[Math.floor(Math.random() * fotosLista.length)];

  // Tamaño aleatorio (conservando proporción)
  const size = 48 + Math.random() * 56; // entre 48 y 104 px de ancho
  img.style.width = `${size}px`;
  img.style.height = 'auto';

  // Posición horizontal aleatoria dentro del viewport
  const pad = 24;
  const x = pad + Math.random() * (window.innerWidth - pad * 2);
  img.style.left = `${x}px`;

  // Variar duración para que no caigan todas igual
  const dur = 3.8 + Math.random() * 2.4; // 3.8s a 6.2s
  img.style.animationDuration = `${dur}s`;

  fallingRoot.appendChild(img);

  // Eliminar al terminar la animación (cuando “cae” fuera de la vista)
  setTimeout(() => img.remove(), dur * 1000 + 200);
}

// Iniciar un bucle que genera nuevas imágenes continuamente
(function iniciarFallingLoop() {
  // Crea una imagen cada ~500–900 ms
  setInterval(() => crearFallingItem(), 500 + Math.random() * 400);
})();
// ==== FIN IMÁGENES CAYENDO ====