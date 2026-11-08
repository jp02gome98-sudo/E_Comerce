
document.addEventListener("DOMContentLoaded", function () {
    const buscador = document.getElementById("buscador");
    const filtros = document.querySelectorAll(".filtro");
    const productos = document.querySelectorAll(".producto");
    const sinResultados = document.getElementById("sin-resultados");

    let categoriaActual = "todos";

    // Buscar y filtrar productos
    function filtrarProductos() {
        const texto = (buscador?.value || "")
            .trim()
            .toLocaleLowerCase("es");

        let visibles = 0;

        productos.forEach(function (producto) {
            const nombre = producto.dataset.nombre || "";
            const categoria = producto.dataset.categoria || "";

            const coincideTexto = nombre.includes(texto);

            const coincideCategoria =
                categoriaActual === "todos" ||
                categoria === categoriaActual;

            const mostrar = coincideTexto && coincideCategoria;

            producto.classList.toggle("oculto", !mostrar);

            if (mostrar) {
                visibles++;
            }
        });

        if (sinResultados) {
            sinResultados.classList.toggle("oculto", visibles > 0);
        }
    }

    // Activar la búsqueda
    if (buscador) {
        buscador.addEventListener("input", filtrarProductos);
    }

    // Filtrar por categoría
    filtros.forEach(function (filtro) {
        filtro.addEventListener("click", function () {
            filtros.forEach(function (otro) {
                otro.classList.remove("activo");
            });

            filtro.classList.add("activo");

            categoriaActual =
                filtro.dataset.categoria || "todos";

            filtrarProductos();
        });
    });

    // Confirmar antes de quitar productos
    document.querySelectorAll("form[data-confirm]").forEach(
        function (formulario) {
            formulario.addEventListener("submit", function (evento) {
                const mensaje =
                    formulario.dataset.confirm ||
                    "¿Deseas continuar?";

                if (!window.confirm(mensaje)) {
                    evento.preventDefault();
                }
            });
        }
    );

    // Ocultar mensajes después de cinco segundos
    const mensajes = document.getElementById("mensajes");

    if (mensajes) {
        window.setTimeout(function () {
            mensajes.querySelectorAll(".mensaje").forEach(
                function (mensaje) {
                    mensaje.style.transition = "opacity .4s";
                    mensaje.style.opacity = "0";

                    window.setTimeout(function () {
                        mensaje.remove();
                    }, 450);
                }
            );
        }, 5000);
    }
});
