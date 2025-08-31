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