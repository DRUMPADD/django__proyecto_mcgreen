$(document).ready(function() {
    $("#form-actualizar").hide();

    $(".modificar_venta").on('click', (e) => {
        const element = $(this)[0].activeElement.parentElement.parentElement;
        // $(this).addClass("clicked");
        $("#form-actualizar").show();

        $("#caja_mensaje").hide();
        var fecha = $(element).find("td").eq(1).text().split("-");
        var cantidad_vieja = ($(element).find("td").eq(5).text()).split(",").join("");

        $("input[name='id_']").val($(element).find("td").eq(0).text());
        $("input[name='id_producto']").val($(element).find("td").eq(7).text());
        $("input[name='fecha_registro']").val(fecha[0] + "-" + fecha[1] + "-" + fecha[2]);
        $("input[name='pozo']").val($(element).find("td").eq(4).text());
        $("input[name='cantidad_antes']").val(parseFloat(cantidad_vieja));
        $("input[name='cantidad_nueva']").val(parseFloat(cantidad_vieja));
        $("input[name='comentario']").val($(element).find("td").eq(8).text());
        e.preventDefault();
    });

    $("#closebtn").on('click', function () {
        $("#form-actualizar").trigger("reset");
        $("#form-actualizar").hide();
    });
});