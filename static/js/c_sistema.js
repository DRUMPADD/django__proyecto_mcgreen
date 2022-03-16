$(document).ready(function () {

    $("#nuevo").hide();
    var contador = 1;
    $("#inicio").text(contador);
    $("#crear_form").click(function () {
        if(contador < 5) {
            ++contador;
            let select_ = $(".producto_select:first").clone();
            select_.addClass("copia_creada");
            select_.find("select[name='sl_producto']").prop("selectedIndex", 0);
            select_.find("select[name='cantidad']").val(parseFloat(0));
            $("#inicio").text(contador);
            select_.insertAfter(".producto_select:last");
        }
    });

    function resetear_formulario() {
        $("form").trigger("reset");
        $(".copia_creada").remove();
    }
    
    $("#eliminar_form").click(function () {
        if(!$(".copia_creada")[0]) {
            contador = 1;
        } else {
            $(".copia_creada").last().remove();
            contador--;
            $("#inicio").text(contador);
        }
    });


    $("#resetear").click(function () {
        $("#nuevo").find("input[name='nuevo_nombre_sistema']").reset();
        if($("#sistema_e").hide()) {
            $("#nuevo").hide();
            $("#sistema_e").show();
        }
    });
    
    $("#nuevo_existente").change(function () {
        if($(this).val() == 'nuevo') {
            let ocultar = $(this).parent();
            ocultar.hide();
            $("#nuevo").show();
            $(this).prop("selectedIndex", 0);
        }
    });

    
    $("form").submit(function (e) {
        var productos = [];
        var prod_rep = new Array();
        var cont_prod = 0;
        e.preventDefault();

        $.each($("select[name='sl_producto'] option:selected"), function () {
            if(!$(this).is("disabled")) {
                ++cont_prod;
                if(productos.indexOf($(this).val()) == -1) {
                    productos.push($(this).val());
                } else {
                    prod_rep.push($(this).val());
                    prod_rep.push($(this).val());
                }
            }
        });
        if(prod_rep.length == 0) {
            if($("select[name='sl_departamentos']").val() != undefined && productos.length == cont_prod) {
                if(($("nombre_sistema").val() != undefined || $("input[name='nuevo_nombre_sistema']").val() != "") || $("input[name='cantidad_sistema']").val() != null) {
                        $.ajax({
                            type: "POST",
                            url: $("#sistema_r").attr("ajax_"),
                            data: $("form").serializeArray(),
                            success: function (response) {
                                swal.fire({
                                    position: 'center',
                                    icon: response.status,
                                    title: response.msg_salida,
                                    showConfirmButton: false,
                                    timer: 2000
                                })
                                resetear_formulario();
                            },
                            error: function(response) {
                                swal.fire({
                                    position: 'center',
                                    icon: "error",
                                    title: response.msg_salida,
                                    showConfirmButton: false,
                                    timer: 2000
                                })
                            }
                        });
                } else {
                    swal.fire({
                        position: 'center',
                        icon: 'error',
                        title: "Debe incluir información del sistema",
                        showConfirmButton: false,
                        timer: 2000
                    })
                }
            } else {
                swal.fire({
                    position: 'center',
                    icon: 'error',
                    title: "Debe seleccionar un departamento",
                    showConfirmButton: false,
                    timer: 2000
                })
            }
        } else {
            swal.fire({
                position: 'center',
                icon: 'error',
                title: "Los productos no deben ser repetidos",
                showConfirmButton: false,
                timer: 2000
            })
        }
    });
});