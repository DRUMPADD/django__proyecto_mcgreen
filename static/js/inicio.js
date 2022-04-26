$(document).ready(function () {
    $("#persona").hide();
    $("#otro_usuario").hide();

    function validar_formulario() {
        $("form input").each(function (indexInArray, valueOfElement) { 
            var inputs_no_vacios = false;
            if($(this).val() == '') {
                inputs_no_vacios = true;
            }
        });
        
        $("form select option:selected").each(function (indexInArray, valueOfElement) { 
            var select_no_vacio = false;
            if($(this).is("disabled")) {
                select_no_vacio = true;
            }
        });

        return inputs_no_vacios && inputs_no_vacios;
    }

    function limpiar_formulario() {
        $("form").trigger("reset");
        $("#persona").hide();
        $("#otro_usuario").hide();
        if($(".usuario_agregado")) {
            $(".usuario_agregado").remove();
        }
    }

    $("input[name='opciones']").click(function () {
        if($(this).val() == 'ACTIVIDAD' || $(this).val() == 'EVENTO') {
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
        const fecha_evento = $("input[name='fecha_evento']").val();
        console.log(!fecha_evento);
        if(validar_formulario() === true) {
            $.ajax({
                method: 'POST',
                url: $("#enviar_evento").attr("data-ajax"),
                data: $("form").serializeArray(),
                success: function (response) {
                    if(response.status == 'success') {
                        limpiar_formulario();
                        swal.fire({
                            position: 'center',
                            icon: response.status,
                            title: response.mensaje,
                            showConfirmButton: false,
                            timer: 4000
                        })
                    } else {
                        swal.fire({
                            position: 'center',
                            icon: response.status,
                            title: response.mensaje,
                            showConfirmButton: false,
                            timer: 4000
                        })
                    }
                }
            })
        } else {
            swal.fire({
                position: 'center',
                icon: "warning",
                title: "Debe llenar todos los campos",
                showConfirmButton: false,
                timer: 4000
            })
        }
    })
});