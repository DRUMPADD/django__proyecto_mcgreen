$(document).ready(function () {
    function recargar_() { 
        $("#puestos").fadeOut("fast").load(location.href + " #puestos>*", "").fadeIn("fast");
    }


    function borrar_valor_usuario() {
        for(let i = 1; i <= 9; i++) {
            $("#funcion" + i).find("input[name='puesto']").val("");
        }
    }

    function saber_seleccionado() {
        $(".funcion").prop("selectedIndex, 0");
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
                    $("#form_crear_perfil").trigger("reset");
                    $("#form_crear_perfil").fadeOut().hide();
                    swal("Datos enviados", res.msg_salida, "success");
                    recargar_();
                } else {
                    swal("Error", res.msg_error, "error");
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


    $("#funcion1").submit(function (e) {
        $.ajax({
            type: "POST",
            url: $("#enviar_funcion1").attr("ajax-data-target"),
            data: $(this).serialize(),
            success: function (response) {
                $("#funcion1").trigger("reset");
                borrar_valor_usuario();
                saber_seleccionado();
                $("#funcion1").hide();
                swal("Éxito!!", response.msg, "success");
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
                $("#funcion2").trigger("reset");
                borrar_valor_usuario();
                saber_seleccionado();
                $("#funcion2").hide();
                swal("Éxito!!", response.msg, "success");
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
                $("#funcion3").trigger("reset");
                borrar_valor_usuario();
                saber_seleccionado();
                $("#funcion3").hide();
                swal("Éxito!!", response.msg, "success");
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
                $("#funcion4").trigger("reset");
                borrar_valor_usuario();
                saber_seleccionado();
                $("#funcion4").hide();
                swal("Éxito!!", response.msg, "success");
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
                $("#funcion5").trigger("reset");
                borrar_valor_usuario();
                saber_seleccionado();
                $("#funcion5").hide();
                swal("Éxito!!", response.msg, "success");
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
                $("#funcion6").trigger("reset");
                borrar_valor_usuario();
                saber_seleccionado();
                $("#funcion6").hide();
                swal("Éxito!!", response.msg, "success");
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
                $("#funcion7").trigger("reset");
                borrar_valor_usuario();
                saber_seleccionado();
                $("#funcion7").hide();
                swal("Éxito!!", response.msg, "success");
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
                $("#funcion8").trigger("reset");
                borrar_valor_usuario();
                saber_seleccionado();
                $("#funcion8").hide();
                swal("Éxito!!", response.msg, "success");
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
                $("#funcion9").trigger("reset");
                borrar_valor_usuario();
                saber_seleccionado();
                $("#funcion9").hide();
                swal("Éxito!!", response.msg, "success");
            }
        });
        e.preventDefault();
    })

    // ?? Directorio
    function recargar__direct() { 
        $("#directorio").fadeOut("fast").load(location.href + " #directorio>*", "").fadeIn("fast");
    }
    $("#form_crear_directorio").hide();

    $("#agregar_directorio").click(() => {
        $("#form_crear_perfil").hide();
        $("#form_crear_directorio").toggle();
    });

    $("#form_crear_directorio").submit((e) => {
        e.preventDefault();
        var respuestas = $("#form_crear_directorio").serializeArray();
        $.ajax({
            type: "POST",
            url: $("#enviar_direc").attr("data-ajax-target"),
            data: respuestas, 
            success: function (res) {
                $("#form_crear_directorio").trigger("reset");
                $("#form_crear_directorio").hide();
                swal(res.bg_msg, res.msg, res.state);
                recargar__direct();
            }
        });
    });

    // ?? Subir imagen
    $("#form_subir_img").hide();

    // $(".mostrar_img").click(function () {
    //     $("#form_subir_img").toggle();
    // });

    // $(".mostrar_img").each(function (index, element) {
    //     // element == this
    //     $(this).click(function () {
    //         $("#form_subir_img").toggle();
    //         var empleado_seleccionado = $(this).parent().parent().find("span:first").text();
    //         $("input[name='empleado_selec']").val(empleado_seleccionado);
    //     });
    // });


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
    //             console.log(data.responseJSON);
    //             console.log("Imagen fallida");
    //         }
    //     });
    // });
});