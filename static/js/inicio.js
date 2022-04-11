$(document).ready(function () {
    $("#persona").hide();
    $("#otro_usuario").hide();

    function limpiar_formulario() {
        $("form").trigger("reset");

        if($(".usuario_agregado")) {
            $(".usuario_agregado").remove();
        }
    }

    $("input[name='opciones']").click(function () {
        if($(this).val() == 'PERSONA EN ESPECIFICO') {
            $("#persona").show();
            $("#otro_usuario").show();
        } else {
            $("#persona").hide();
            $("#otro_usuario").hide();
        }
    });


    $("#btn_cerrar_opc1").click(function () {
        let elemento_padre_opc1 = $(this).parent();
        console.log(elemento_padre_opc1.html());
        elemento_padre_opc1.find(".usuario").prop("selectedIndex", 0);
        elemento_padre_opc1.find(".usuario_agregado").remove();
        $("input[name='opciones']").prop('checked', false);
        elemento_padre_opc1.hide();
    });

    $("#otro_usuario").click(function () {
        let usuario = $(".usuario:first").clone();
        usuario.addClass("usuario_agregado");
        usuario.prop("selectedIndex", 0);
        usuario.insertAfter(".usuario:last");
    });

    $("form").submit(function (e) {
        e.preventDefault();
        $.ajax({
            method: 'POST',
            url: $("#enviar_evento").attr("data-ajax"),
            data: $("form").serializeArray(),
            success: function (response) {
                if(response.status == 'success') {
                    $("form").trigger("reset");
                    alert(response.mensaje);
                } else {
                    alert(response.mensaje);
                }
            }
        })
    })
});