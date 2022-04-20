$(document).ready(function () {
    // Función para recargar div con id puestos
    function recargar_() { 
        $("#puestos").fadeOut("fast").load(location.href + " #puestos>*", "").fadeIn("fast");
    }

    function borrar_valor_usuario() {
        for(let i = 1; i <= 9; i++) {
            $("#funcion" + i).find("input[name='puesto']").val("");
        }
    }

    function saber_seleccionado() {
        $("select.sl_funcion").prop("selectedIndex", 0);
    }


    function ocultar_formularios() {
        for(let i = 1; i < 9; i++) {
            $("#funcion" + i).hide();
        }
        for(let i = 1; i < 9; i++) {
            $("#funcion" + i).trigger("reset");
        }
    }
    
    function ocultar_formularios_img() {
        $("#form_subir_img").hide();
    }

    borrar_valor_usuario();
    $("#form_crear_perfil").hide();
    $(".funcion").hide();
    $("#agregar").click(() => {
        $("#form_crear_directorio").hide();
        $("#form_crear_perfil").toggle();
    })

    $("#form_crear_perfil").submit((e) => {
        e.preventDefault();
        var respuestas = $("#form_crear_perfil").serializeArray();
        $.ajax({
            type: "POST",
            url: $("#enviar_puesto").attr("data-ajax-target"),
            data: respuestas, 
            success: function (res) {
                if(res.msg == 'VACANTES AÑADIDAS AL PUESTO') {
                    saber_seleccionado();
                    $("#form_crear_perfil").trigger("reset");
                    $("#form_crear_perfil").fadeOut().hide();
                    swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: res.msg_salida,
                        showConfirmButton: false,
                        timer: 2000
                    })
                    // swal("Datos enviados", res.msg_salida, "success");
                    recargar_();
                } else {
                    swal.fire({
                        position: 'center',
                        icon: 'error',
                        title: res.msg_error,
                        showConfirmButton: false,
                        timer: 2000
                    })
                    // swal("Error", res.msg_error, "error");
                }
            }
        });
    });

    $("select.sl_funcion").change(function (i) {
        var $this = $(this);
        var usuario = $this.parent().parent().parent().find("span:first").text();
        var nombre_puesto = $this.parent().parent().parent().find("span:last").text();
        $(".funcion").hide();
        $("#" + $(this).val()).show();
        for(let i = 0; i < 9; i++) {
            $("#" + $(this).val()).find("p").text(nombre_puesto);
            $("#" + $(this).val()).find("input[name='puesto']").val(usuario);
        }
        ocultar_formularios_img();
    });

    var botones_cerrar = $(".btn_cerrar");
    var form_cerrar = $(".funcion");
    $.each(botones_cerrar, function (i) {
        var selects = $("select.sl_funcion");
        var $boton = $(this);
        $boton.click(function() {
            $(".funcion").each((index) => {
                $(form_cerrar[index]).hide();
                borrar_valor_usuario();
                $(selects[i]).prop("selectedIndex", 0);
            });
        });
    });


    // $.each($(".formulario"), function (index) {
    //     $(this).submit(function (e) {
    //         e.preventDefault();
    //         $(".formulario").trigger("reset");
    //         $.ajax({
    //             type: "POST",
    //             url: $(this).find("input[name='enviar_funcion']").attr("ajax-data-target"),
    //             data: $(this).serialize(),
    //             success: function (response) {
    //                 saber_seleccionado();
    //                 ocultar_formularios();
    //                 borrar_valor_usuario();
    //                 swal.fire({
    //                     position: 'center',
    //                     icon: 'success',
    //                     title: response.msg,
    //                     showConfirmButton: false,
    //                     timer: 2000
    //                 })
    //                 // swal("Éxito!!", response.msg, "success");
    //             }
    //         });
    //     });
    // });

    $("#funcion1").submit(function (e) {
        $.ajax({
            type: "POST",
            url: $("#enviar_funcion1").attr("ajax-data-target"),
            data: $(this).serialize(),
            success: function (response) {
                saber_seleccionado();
                ocultar_formularios();
                borrar_valor_usuario();
                swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: response.msg,
                    showConfirmButton: false,
                    timer: 2000
                })
                // swal("Éxito!!", response.msg, "success");
            }
        });
        e.preventDefault();
    })
    $("#funcion2").submit(function (e) {
        $.ajax({
            type: "POST",
            url: $("#enviar_funcion2").attr("ajax-data-target"),
            data: $(this).serialize(),
            success: function (response) {
                saber_seleccionado();
                ocultar_formularios();
                borrar_valor_usuario();
                swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: response.msg,
                    showConfirmButton: false,
                    timer: 2000
                })
                // swal("Éxito!!", response.msg, "success");
            }
        });
        e.preventDefault();
    })
    $("#funcion3").submit(function (e) {
        $.ajax({
            type: "POST",
            url: $("#enviar_funcion3").attr("ajax-data-target"),
            data: $(this).serialize(),
            success: function (response) {
                saber_seleccionado();
                ocultar_formularios();
                borrar_valor_usuario();
                swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: response.msg,
                    showConfirmButton: false,
                    timer: 2000
                })
                // swal("Éxito!!", response.msg, "success");
            },
            error: function () {
                swal.fire({
                    position: 'center',
                    icon: 'error',
                    title: response.msg,
                    showConfirmButton: false,
                    timer: 2000
                })
                // swal("Error", response.msg, "error");
            }
        });
        e.preventDefault();
    })
    $("#funcion4").submit(function (e) {
        $.ajax({
            type: "POST",
            url: $("#enviar_funcion4").attr("ajax-data-target"),
            data: $(this).serialize(),
            success: function (response) {
                saber_seleccionado();
                ocultar_formularios();
                borrar_valor_usuario();
                swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: response.msg,
                    showConfirmButton: false,
                    timer: 2000
                })
                // swal("Éxito!!", response.msg, "success");
            }
        });
        e.preventDefault();
    })
    $("#funcion5").submit(function (e) {
        $.ajax({
            type: "POST",
            url: $("#enviar_funcion5").attr("ajax-data-target"),
            data: $(this).serialize(),
            success: function (response) {
                saber_seleccionado();
                ocultar_formularios();
                borrar_valor_usuario();
                swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: response.msg,
                    showConfirmButton: false,
                    timer: 2000
                })
                // swal("Éxito!!", response.msg, "success");
            }
        });
        e.preventDefault();
    })
    $("#funcion6").submit(function (e) {
        $.ajax({
            type: "POST",
            url: $("#enviar_funcion6").attr("ajax-data-target"),
            data: $(this).serialize(),
            success: function (response) {
                saber_seleccionado();
                ocultar_formularios();
                borrar_valor_usuario();
                swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: response.msg,
                    showConfirmButton: false,
                    timer: 2000
                })
                // swal("Éxito!!", response.msg, "success");
            }
        });
        e.preventDefault();
    })
    $("#funcion7").submit(function (e) {
        $.ajax({
            type: "POST",
            url: $("#enviar_funcion7").attr("ajax-data-target"),
            data: $(this).serialize(),
            success: function (response) {
                saber_seleccionado();
                ocultar_formularios();
                borrar_valor_usuario();
                swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: response.msg,
                    showConfirmButton: false,
                    timer: 2000
                })
                // swal("Éxito!!", response.msg, "success");
            }
        });
        e.preventDefault();
    })
    $("#funcion8").submit(function (e) {
        $.ajax({
            type: "POST",
            url: $("#enviar_funcion8").attr("ajax-data-target"),
            data: $(this).serialize(),
            success: function (response) {
                saber_seleccionado();
                ocultar_formularios();
                borrar_valor_usuario();
                swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: response.msg,
                    showConfirmButton: false,
                    timer: 2000
                })
                // swal("Éxito!!", response.msg, "success");
            }
        });
        e.preventDefault();
    })
    $("#funcion9").submit(function (e) {
        $.ajax({
            type: "POST",
            url: $("#enviar_funcion9").attr("ajax-data-target"),
            data: $(this).serialize(),
            success: function (response) {
                saber_seleccionado();
                ocultar_formularios();
                borrar_valor_usuario();
                swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: response.msg,
                    showConfirmButton: false,
                    timer: 2000
                })
                // swal("Éxito!!", response.msg, "success");
            }
        });
        e.preventDefault();
    })
    
    // ?? Directorio del personal

    function recargar__direct() { 
        $("#directorio").fadeOut("fast").load(location.href + " #directorio>*", "").fadeIn("fast");
    }
    $("#form_crear_directorio").hide();

    $("#form_crear_directorio").submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: $("#enviar_direc").attr("data-ajax-target"),
            data: $("#form_crear_directorio").serializeArray(), 
            success: function (res) {
                switch(res.state) {
                    case 'success':
                        saber_seleccionado();
                        $("#form_crear_directorio").trigger("reset");
                        $("#form_crear_directorio").hide();
                        swal.fire({
                            position: 'center',
                            icon: res.state,
                            title: res.msg,
                            showConfirmButton: false,
                            timer: 2000
                        })
                        recargar__direct();
                        break;
                    default:
                        swal.fire({
                            position: 'center',
                            icon: res.state,
                            title: res.msg,
                            showConfirmButton: false,
                            timer: 4000
                        })
                        break;
                    }
            }
        });

        // if(id_p_select == "" || id_p_select === undefined || id_p_select === null) {
        //     swal("Error", "Debe seleccionar un puesto", "error");
        // } else {
        //     var respuestas = $("#form_crear_directorio").serializeArray();
        //     $.ajax({
        //         type: "POST",
        //         url: $("#enviar_direc").attr("data-ajax-target"),
        //         data: respuestas, 
        //         success: function (res) {
        //             saber_seleccionado();
        //             $("#form_crear_directorio").trigger("reset");
        //             $("#form_crear_directorio").hide();
        //             swal.fire({
        //                 position: 'center',
        //                 icon: res.state,
        //                 title: res.msg,
        //                 showConfirmButton: false,
        //                 timer: 2000
        //             })
        //             // swal(res.bg_msg, res.msg, res.state);
        //             recargar__direct();
        //         }
        //     });
        // }
    });

    $("#agregar_directorio").click(() => {
        $("#form_crear_perfil").hide();
        $("#form_crear_directorio").toggle();
    });


    // ?? Subir imagen
    $("#form_subir_img").hide();

    // $(".mostrar_img").click(function () {
    //     $("#form_subir_img").toggle();
    // });

    $(".mostrar_img").each(function (index, element) {
        // element == this
        $(this).click(function () {
            $("#form_subir_img").toggle();
            var empleado_seleccionado = $(this).parent().parent().find("span:first").text();
            var nombre_emp = $(this).parent().parent().find("span:last").text();
            $("input[name='empleado_selec']").val(empleado_seleccionado);
            $("#nombre_emp").text(nombre_emp),
            ocultar_formularios();
        });
    });


    // $("#form_subir_img").submit(function (e) {
    //     e.preventDefault();
    //     var img_data = $("input[name='img_']").get(0).files[0];
    //     var empleado = $("input[name='empleado_selec']").val();
    //     formdata = new FormData();
    //     formdata.append("imagen", img_data);
    //     formdata.append("empleado", empleado);
    //     var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    //     $.ajax({
    //         type: "POST",
    //         url: $("#imagen_enviar").attr("dato-ajax"),
    //         headers:{
    //             "X-CSRFToken": csrftoken
    //         },
    //         data: formdata,
    //         cache : false,
    //         contentType : false,
    //         processData: false,
    //         async: false,
    //         success: function (response) {
    //             if(response.msg === "Exito") {
    //                 $(this).trigger("reset");
    //                 $(this).hide();
    //                 swal(response.msg, response.msg_salida, response.status);
    //             } else {
    //                 swal(response.msg, response.msg_salida, response.status);
    //             }
    //         },
    //         error: function (data) {
    //         }
    //     });
    // });

});
