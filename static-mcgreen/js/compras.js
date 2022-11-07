$(document).ready(function () {
    var contador = 1;
    if(!document.getElementsByClassName(".campo_creado")) {
        contador = 1;
    }

    function recargar_proveedores() {

    }

    $("#btnAddForm").click(function () {
        contador = contador + 1;
        var $formulario = $(".articulos:first").clone();
        $formulario.trigger("reset");
        $formulario.addClass("campo_creado");
        $formulario.find(".comprador").hide();
        $formulario.find(".fecha").hide();
        $formulario.find(".motivo").hide();
        $formulario.find("input[name='motivo']").val("");
        $formulario.find("input[name='articulo']").val(contador);
        $formulario.find("input[name='cantidad']").val("");
        $formulario.find("input[name='densidad']").val(1);
        $formulario.find("input[name='p_u']").val("");
        $formulario.insertAfter(".agrega_articulo .articulos:last");
    });
    
    $("#btnDeleteForm").click(function (e) {
        if(!$(".campo_creado")[0]) {
            contador = 1;
        } else {
            $(".campo_creado").last().remove();
            contador--;
        }
    });
    
    $("#form_compra").submit(function(e) {
        e.preventDefault();
        
        let proveedores = Array();
        $("select[name='sl_proveedores']").each(function() {
            if($(this).val() !== null) {
                proveedores.push($(this).val());
            }
        });
        
        var fecha_c = $("input[name='fecha_compra']").val();
        var motivo_ = $("input[name='motivo']").val();
        
        let productos = Array();
        $("select[name='sl_productos']").each(function() {
            if($(this).val() !== null) {
                productos.push($(this).val());
            }
        });
        
        let cantidades = Array();
        $("input[name='cantidad']").each(function() {
            if($(this).val() !== null) {
                productos.push($(this).val());
            }
        });

        let precios = Array();
        $("input[name='p_u']").each(function() {
            if($(this).val() !== null) {
                precios.push($(this).val());
            }
        });

        if(proveedores.length !== 0 && productos !== 0 && cantidades !== 0 && precios !== 0 && fecha_c !== "" & motivo_ !== "") {
            $.ajax({
                type: "POST",
                url: $("#enviar_formulario").attr("ajax-data-target"),
                data: $("#form_compra").serializeArray(),
                success: function (response) {
                    if(response.status == 'success') {
                        $(".campo_creado").remove();
                        $("#form_compra").trigger("reset");
                        swal.fire({
                            position: 'center',
                            icon: response.status,
                            title: response.msg_compra,
                            showConfirmButton: false,
                            timer: 3000
                        })
                    } else {
                        swal.fire({
                            position: 'center',
                            icon: response.status,
                            title: response.msg_compra,
                            showConfirmButton: false,
                            timer: 3000
                        })
                    }
                }
            });
        } else {
            swal("Error","Debe llenar todos los campos", "error");
        }
    });


    $("#form_provee").submit(function (e) {
        e.preventDefault();
        var respuestas = $(this).serializeArray();
        $.ajax({
            type: "POST",
            url: $("#enviar_provee").attr("dato-ajax"),
            data: respuestas,
            success: function (response) {
                switch(response.status) {
                    case 'success':
                        $("#form_provee").trigger("reset");
                        swal.fire({
                            position: 'center',
                            icon: response.status,
                            title: response.msg_salida,
                            showConfirmButton: false,
                            timer: 3000
                        })
                        break;
                    case 'error':
                        swal.fire({
                            position: 'center',
                            icon: response.status,
                            title: response.msg_salida,
                            showConfirmButton: false,
                            timer: 3000
                        })
                            break;
                    case 'warning':
                        swal.fire({
                            position: 'center',
                            icon: response.status,
                            title: response.msg_salida,
                            showConfirmButton: false,
                            timer: 3000
                        })
                            break;
                }
            }
        });
    });
});