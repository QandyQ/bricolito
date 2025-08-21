const envoltura = document.querySelector(".envoltura-sobre");
const carta = document.querySelector(".carta");

document.addEventListener("click", (e) => {
    // Busca la envoltura-sobre más cercana al clic
    const envoltura = e.target.closest(".envoltura-sobre");
    const carta = envoltura ? envoltura.querySelector(".carta") : null;

    if (
        envoltura &&
        (e.target.matches(".sobre") ||
        e.target.matches(".solapa-derecha") ||
        e.target.matches(".solapa-izquierda") ||
        e.target.matches(".corazon"))
    ) {
        envoltura.classList.toggle("abierto");
    } else if (envoltura && e.target.matches(".sobre *")) {
        if (carta && !carta.classList.contains("abierta")) {
            carta.classList.add("mostrar-carta");

            setTimeout(() => {
                carta.classList.remove("mostrar-carta");
                carta.classList.add("abierta");
            }, 500);
            envoltura.classList.add("desactivar-sobre")
        } else if (carta) {
            carta.classList.add("cerrando-carta");
            envoltura.classList.remove("desactivar-sobre");

            setTimeout(() => {
                carta.classList.remove("cerrando-carta")
                carta.classList.remove("abierta")
            }, 500);
        }
    }
});