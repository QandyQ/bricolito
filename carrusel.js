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