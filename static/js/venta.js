// Inicializa los valores
var productosSeleccionados = [];
let metodoPagoSeleccionado = "";

// Función para formatear números a CLP
function formatearCLP(numero) {
    return `CLP ${numero.toLocaleString('es-CL', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
}

// Evento al cargar el documento
document.addEventListener("DOMContentLoaded", function () {
    const btnPago = document.getElementById("btn-Pago");
    const modalPago = new bootstrap.Modal(document.getElementById("modalPago"));

    // Evento para abrir el modal al hacer clic en el botón de pago
    btnPago.addEventListener("click", function (event) {
        event.preventDefault();
        modalPago.show();
    });

    // Actualiza el método de pago al hacer clic en una opción de pago
    document.querySelectorAll('.opcion-pago').forEach(function (pago) {
        pago.addEventListener('click', function () {
            metodoPagoSeleccionado = this.getAttribute('data-value');  // Asigna el valor seleccionado
            document.getElementById('form-datos').style.display = 'block';
            document.getElementById('input-rut').style.display = metodoPagoSeleccionado === 'Transferencia' ? 'block' : 'none';
        });
    });

    // Confirmación del método de pago
    document.getElementById("confirmarPago").addEventListener("click", function () {
        if (metodoPagoSeleccionado) {
            modalPago.hide();
            alert("Método de pago seleccionado: " + metodoPagoSeleccionado);
        } else {
            alert("Por favor selecciona un método de pago");
        }
    });
});

// Función para actualizar la tabla de productos seleccionados
function actualizarTabla() {
    const tbody = document.querySelector('tbody');
    tbody.innerHTML = '';

    let total = 0;
    productosSeleccionados.forEach((producto, index) => {
        const subtotal = producto.precio * producto.cantidad;
        total += subtotal;
        const row = `
            <tr>
                <td>${index + 1}</td>
                <td>${producto.nombre}</td>
                <td>${producto.cod}</td>
                <td>${formatearCLP(producto.precio)}</td> <!-- Muestra el precio con descuento en CLP -->
                <td>${producto.cantidad}</td>
                <td>${formatearCLP(subtotal)}</td> <!-- Muestra el subtotal en CLP -->
                <td><button class="deleteproducto btn btn-danger" data-id="${producto.cod}">Eliminar</button></td>
            </tr>
        `;
        tbody.insertAdjacentHTML('beforeend', row);
    });

    document.querySelector('.d-flex h5 span').textContent = formatearCLP(total); // Total en CLP
}

// Evento para agregar productos al carrito
document.addEventListener('click', function (event) {
    if (event.target && event.target.id === 'agregar-carrito') {
        const productoId = event.target.getAttribute('producto_id');
        const nombre = event.target.closest('.card').querySelector('.nombre').textContent;
        const precio = parseFloat(event.target.closest('.card').querySelector('.precio').textContent.replace('$', '').replace('.', '').trim());
        const stock = parseInt(event.target.getAttribute('data-stock'));
        const descuento = parseFloat(event.target.closest('.card').querySelector('.descuento').textContent.replace('%', '')) || 0;

        // Calcula el precio con descuento
        const precioConDescuento = precio - (precio * (descuento / 100));

        let producto = productosSeleccionados.find(p => p.cod === productoId);

        if (producto) {
            if (producto.cantidad < stock) {
                producto.cantidad += 1;
            } else {
                alert("No puedes agregar más de este producto, has alcanzado el stock máximo.");
            }
        } else {
            if (stock > 0) {
                productosSeleccionados.push({
                    cod: productoId,
                    nombre: nombre,
                    precio: precioConDescuento, // Guardamos el precio con descuento
                    cantidad: 1
                });
            } else {
                alert("Este producto no tiene stock disponible.");
            }
        }

        actualizarTabla();
    }
});

// Evento para eliminar productos del carrito
document.addEventListener('click', function (event) {
    if (event.target && event.target.classList.contains('deleteproducto')) {
        const productoId = event.target.getAttribute('data-id');
        productosSeleccionados = productosSeleccionados.filter(p => p.cod !== productoId);
        actualizarTabla();
    }
});

// Evento para generar la venta
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector('#generar-venta').replaceWith(document.querySelector('#generar-venta').cloneNode(true));
    document.querySelector('#generar-venta').addEventListener('click', function (event) {
        console.log("Botón Generar Venta clickeado");

        // Validación del método de pago
        if (!metodoPagoSeleccionado) {
            alert("Por favor selecciona un método de pago antes de generar la venta.");
            console.log("Método de pago no seleccionado. Deteniendo ejecución.");
            event.preventDefault();
            return false;
        }

        // Validación del carrito de productos
        const totalAPagar = parseFloat(document.querySelector('.d-flex h5 span').textContent.replace('CLP ', '').replace('.', ''));
        if (isNaN(totalAPagar) || totalAPagar <= 0) {
            alert("Seleccione al menos 1 producto.");
            console.log("Total no válido. Deteniendo ejecución.");
            event.preventDefault();
            return false;
        }

        const productos = {};
        document.querySelectorAll('tbody tr').forEach(row => {
            const productoId = row.querySelector('.deleteproducto').getAttribute('data-id');
            const cantidad = parseInt(row.querySelector('td:nth-child(5)').textContent);
            productos[productoId] = cantidad;
        });

        if (Object.keys(productos).length === 0) {
            alert("No hay productos en el carrito. Agrega productos antes de generar la venta.");
            console.log("Carrito vacío. Deteniendo ejecución.");
            event.preventDefault();
            return false;
        }

        // Confirmación antes de generar la venta
        console.log("Método de pago y productos verificados, procediendo con la generación de venta.");

        const csrftoken = document.querySelector('[name=csrf-token]').content;

        console.log("Generando venta...");  // Verifica que llegue a este punto
        fetch('/generar-venta/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                total: totalAPagar,
                productos: productos,
                metodo_pago: metodoPagoSeleccionado
            })
        })
        .then(response => {
            console.log("Respuesta del servidor:", response);  // Muestra la respuesta completa en consola
            if (response.ok) {
                alert("Venta generada con éxito con el método de pago: " + metodoPagoSeleccionado);
                console.log("Venta generada exitosamente.");
                exportarBoletaAPDF();  // Genera el PDF solo después de una respuesta exitosa
                location.reload();
            } else {
                alert("Error al generar la venta");
                console.log("Error al generar la venta. Estado:", response.status, response.statusText);
            }
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
            alert("Ocurrió un error al intentar generar la venta");
        });
    });
});
