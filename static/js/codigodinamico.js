function generarCodigoVenta() {

  const numeroAleatorio = Math.floor(1000 + Math.random() * 9000);
  const codigoVenta = `${numeroAleatorio}`;
  document.getElementById("codigodinamico").querySelector("span").textContent = codigoVenta;
}
window.onload = generarCodigoVenta;


function exportarBoletaAPDF() {
  console.log("Función de descarga activada por el botón correcto");

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  // Obtener los datos de la venta y cliente
  const numeroSerie = document.getElementById('codigodinamico').querySelector('span').textContent;
  const idCliente = document.getElementById('cliente-id').value;
  const nombreCliente = document.getElementById('cliente-nombre').value;
  const totalAPagar = document.querySelector('.d-flex h5 span').textContent;

  // Configuración del documento PDF
  doc.setFontSize(18);
  doc.text('Boleta Electrónica', 10, 10);
  doc.setFontSize(12);
  doc.text(`NRO. SERIE: ${numeroSerie}`, 10, 20);
  doc.text(`ID Cliente: ${idCliente}`, 10, 30);
  doc.text(`Nombre Cliente: ${nombreCliente}`, 10, 40);
  doc.text(`Método de Pago: ${metodoPagoSeleccionado}`, 10, 50);

  // Detalle de productos
  const productos = [];
  $('tbody tr').each(function () {
      const nro = $(this).find('td:nth-child(1)').text();
      const nombre = $(this).find('td:nth-child(2)').text();
      const cod = $(this).find('td:nth-child(3)').text();
      const precio = $(this).find('td:nth-child(4)').text();
      const cantidad = $(this).find('td:nth-child(5)').text();
      const total = $(this).find('td:nth-child(6)').text();
      productos.push([nro, nombre, cod, precio, cantidad, total]);
  });

  doc.text('Detalle de Productos:', 10, 60);
  doc.autoTable({
      head: [['NRO', 'PRODUCTO', 'COD', 'PRECIO', 'CANT', 'TOTAL']],
      body: productos,
      startY: 70,
  });

  // Total a pagar
  doc.text(`Total a Pagar: $${totalAPagar}`, 10, doc.lastAutoTable.finalY + 10);

  // Guardar el PDF
  doc.save(`${numeroSerie}.pdf`);
}
