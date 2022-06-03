$(document).ready(function () {
    const ctx = document.getElementById('detalles_rrhh').getContext('2d');
    $("#table").hide();
    $("#principal").show();
    $.ajax({
        type: "GET",
        url: $("#url_rrhh").attr("ajax-get"),
        success: function (response) {
            let detalles = response.msg;
            let datasets = [];
            let total_e = 0, total_p = 0;
            let tbody_ = $("#tbody_emp");

            detalles.map((d, i) => {
                const red_ = `${Math.floor(Math.random() * (255 - 1) + 1)}`;
                const green_ = `${Math.floor(Math.random() * (255 - 1) + 1)}`;
                const blue_ = `${Math.floor(Math.random() * (255 - 1) + 1)}`;
                const rgb_random = `rgba(${red_}, ${green_}, ${blue_}, .3)`;
                const rgb_border = `rgba(${red_}, ${green_}, ${blue_}, .5)`;
                total_e += d[0]
                datasets.push({
                    label: d[1],
                    data: [d[0]],
                    backgroundColor: rgb_random, // Color de fondo
                    borderColor: rgb_border, // Color del borde
                    borderWidth: 3,// Ancho del borde
                    tension: .5,
                    fill: true,
                })

                tbody_.append(`
                    <tr>
                        <td>${d[1]}</td>
                        <td>${d[0]}</td>
                    </tr>
                `)

                if(d[1]) {
                    total_p += 1;
                }
            });

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['PUESTOS'],
                    datasets 
                },
                options: {
                    scales: {
                        yAxes: {
                            display: true,
                            ticks: {
                                beginAtZero: true,
                                steps: 10,
                                stepValue: 5,
                                max: total_e
                            }
                        }
                    }
                }
            });

            $("#table").show();
            $("#emp_reg").text(total_e);
            $("#emp_total").text(response.total_empleados);
            $("#ptos_reg").text(total_p);
            $("#ptos_total").text(response.total_puestos);
        }
    });
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
        $("#principal").toggle();
    }
    
    function ocultar_formularios_img() {
        $("#form_subir_img").hide();
        $("#principal").show();
    }

    borrar_valor_usuario();
    $("#form_crear_perfil").hide();
    $(".funcion").hide();
    $("#agregar").click(() => {
        $("#form_crear_directorio").hide();
        $("#form_crear_perfil").toggle();
        $("#principal").toggle();
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
        $("#principal").hide();
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
            $("#principal").show();
        });
    });


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
    $("input[name='fec_nac']").change(function () {
        var fecha_hoy = new Date();
        var dia_hoy = fecha_hoy.getDate();
        var mes_hoy = fecha_hoy.getMonth() + 1;
        var anio_hoy = fecha_hoy.getFullYear();
        var fecha = $(this).val().split("-");
        
        var dia_elegida = fecha[2];
        var mes_elegida =  fecha[1];
        var anio_elegida = fecha[0];
        var edad = anio_hoy - anio_elegida;
        if(mes_elegida > mes_hoy) {
            $("input[name='edad']").val(edad - 1);
        } else if (mes_elegida == mes_hoy) {
            if(dia_elegida <= dia_hoy) {
                $("input[name='edad']").val(edad);
                console.log(edad);
            } else {
                $("input[name='edad']").val(edad - 1);
            } 
        } else if (mes_elegida < mes_hoy) {
            if(dia_elegida <= dia_hoy) {
                $("input[name='edad']").val(edad);
            } else {
                $("input[name='edad']").val(edad - 1);
            }
        } else {
            $("input[name='edad']").val(edad - 1);
        }
    });

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
        $("#principal").toggle();
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
            $("#principal").toggle();
            var empleado_seleccionado = $(this).parent().parent().find("span:first").text();
            var nombre_emp = $(this).parent().parent().find("span:last").text();
            $("input[name='empleado_selec']").val(empleado_seleccionado);
            $("#nombre_emp").text(nombre_emp),
            ocultar_formularios();
        });
    });

    $("#form_subir_img").submit(function (e) {
        e.preventDefault();
        if(window.FormData !== undefined) {
            var formData = new FormData(this);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', $("#_enviar").attr('dato-ajax'), true);
            xhr.setRequestHeader('X-REQUESTED-WITH', 'XMLHttpRequest')            
            xhr.onreadystatechange = async function() {
                if(xhr.readyState == 4) {
                    if(xhr.status == 200) {
                        res = JSON.parse(xhr.responseText);
                        // Code for success upload
                        if(res.status == 'success') {
                            // await alert("Resultado: " + res.msg);
                            await swal.fire({
                                position: 'center',
                                icon: res.status,
                                title: res.msg,
                                showConfirmButton: false,
                                timer: 3000
                            })
                            $("form").trigger("reset");
                            location.reload(true);
                        } else {
                            // await alert("Resultado: " + res.msg);
                            await swal.fire({
                                position: 'center',
                                icon: res.status,
                                title: res.msg,
                                showConfirmButton: false,
                                timer: 3000
                            })
                        }
                    }
                    else {
                        swal.fire({
                            position: 'center',
                            icon: "error",
                            title: "Error en el sistema",
                            showConfirmButton: false,
                            timer: 3000
                        })
                    }
                }
            };
            xhr.send(formData);
        } else {
            swal.fire({
                position: 'center',
                icon: "error",
                title: "Error al enviar los datos",
                showConfirmButton: false,
                timer: 3000
            })
        }
    });

});
