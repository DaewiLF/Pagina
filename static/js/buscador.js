
$(document).ready(function () {
    $('#buscador').on('keyup', function () {
        var searchText = $(this).val().toLowerCase().trim();

        $('.producto_fila').each(function () {
            var nombre = $(this).find('.nombre').text().toLowerCase();
            var precio = $(this).find('.precio').text().toLowerCase();
            var stock = $(this).find('.stock').text().toLowerCase();
            var descuento = $(this).find('.descuento').text().toLowerCase();

            if (nombre.includes(searchText) ||
                precio.includes(searchText) ||
                stock.includes(searchText) ||
                descuento.includes(searchText)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});