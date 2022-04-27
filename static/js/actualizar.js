$(document).ready(function() {
    $("#form-actualizar").hide();

    $(".modificar_venta").on('click', (e) => {
        const element = $(this)[0].activeElement.parentElement.parentElement;
        // $(this).addClass("clicked");
        $("#form-actualizar").show();

        $("#caja_mensaje").hide();
        

        $("input[name='id_']").val($(element).find("td").eq(0).text());
        $("input[name='fecha_registro']").val($(element).find("td").eq(1).text());
        $("input[name='pozo']").val($(element).find("td").eq(3).text());
        e.preventDefault();
    });

    $("#closebtn").on('click', function () {
        $("#form-actualizar").trigger("reset");
        $("#form-actualizar").hide();
    });
});