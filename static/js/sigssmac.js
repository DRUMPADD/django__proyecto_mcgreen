$(document).ready(async function () {
    function validarFormulario(formulario) {
        const inputs = $(formulario + " input").filter(function () {
            return $(this).val() == '';
        }).length;

        let check_cli_pro = $(formulario);
        if(check_cli_pro.has("input[type='checkbox']")) {
            check_cli_pro = check_cli_pro.find("input[type='checkbox']");
            if(check_cli_pro.is(":checked")) {
                let textarea_direccion = $(formulario).find("textarea[name='direccion']");
                console.log("Es todo o nada");
                return inputs == 0 && textarea_direccion.val() != '';
            } else {
                console.log("Es todo o nada 2");
                return inputs == 0;
            }
        }
    }

    await $("input[name='fecha_compromiso']").hide();
    await $("#btnVolver").hide();
    await $("#direccion").hide();
    $("select[name='sl_fecha']").change(function() {
        if($(this).val() == 'fecha') {
            $("input[name='fecha_compromiso']").toggle();
            $("input[name='fecha_compromiso']").removeAttr("type");
            $("input[name='fecha_compromiso']").attr("type", "date");
            $("select[name='sl_fecha']").hide();
            $("#btnVolver").show();
        }
        if($(this).val() == 'INMEDIATA') {
            $("input[name='fecha_compromiso']").removeAttr("type");
            $("input[name='fecha_compromiso']").attr("type", "text");
            $("input[name='fecha_compromiso']").val('INMEDIATA');
            $("#btnVolver").show();
        }
    });

    $("#btnVolver").click(() => {
        $("select[name='sl_fecha']").prop('selectedIndex', 0);
        $("select[name='sl_fecha']").show();
        $("#btnVolver").toggle();
        if($("input[name='fecha_compromiso']").show()) {
            $("input[name='fecha_compromiso']").toggle();
        }
    });
    $("#form_sigssmac").submit(function (e) {
        e.preventDefault();
        var cont_inputs = $('#form_sigssmac input').filter(function(){
            var this_i = $(this);
            if(this_i.attr("name") != 'herramientas') {
                return this_i.val() == '';
            }
        }).length;
        var selects = $('#form_sigssmac select').filter(function(){
            var this_sl = $(this);
            if(this_sl.attr("name") != 'sl_afecta') {
                return this_sl.val() == null;
            }
        }).length;
        console.log(cont_inputs);
        console.log(selects);
        if(cont_inputs == 0 && $("#form_sigssmac textarea").val().trim() != '' && selects == 0 && $("#form_sigssmac input[name='hallazgos']").val() != '') {
            if(window.FormData !== undefined) {
                var formData = new FormData(this);
                var xhr = new XMLHttpRequest();
                xhr.open('POST', $("#enviar_sigssmac").attr('ajax'), true);
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
                            console.log("No se pudo");
                            // Code for error
                        }
                    }
                };
                xhr.send(formData);
            } else {
                console.log("No existe");
            }
        } else {
            swal.fire({
                position: 'center',
                icon: "warning",
                title: "Debe llenar todos los campos",
                showConfirmButton: false,
                timer: 3000
            })
        }
    });

    $(".ver_img").each(function(index) {
        var $this_ = $(this);
        $this_.click(async function () {
            var div_display = $("#display_i");
            var img_src = $("#img_mostrar");
            let src_ = $this_.attr("src-img");
            if(src_ == 'media/img/None') {
                await swal.fire({
                    position: 'center',
                    icon: "error",
                    title: "No existe imagen",
                    showConfirmButton: false,
                    timer: 3000
                })
            } else {
                img_src.attr("src", src_);
                await img_src.show();
                await div_display.css("display", "block");
            }

        });
    });
    
    $(".close").each(function () {
        var $this_ = $(this);
        $this_.click(function () {
            $this_.parent().parent().hide();
        });
    });

    $(".btnSubirImg").each(function () {
        var this_ = $(this);
        this_.click(function () {
            let btnSubir = this_.parent().parent();
            const getId = btnSubir.find("td").eq(0).text();
            let inp_sigss = $("input[name='sigss_id']");
            inp_sigss.val(getId);
            console.log(inp_sigss.val());
            $("#form_subir_ev").show();
        });
    });

    await $("#form_subir_ev").hide();
    $("#form_subir_ev").submit(function (e) {
        e.preventDefault();
        if($("input[name='evidencia_despues']").val() != '') {
            if(window.FormData !== undefined) {
                var formData = new FormData(this);
                var xhr = new XMLHttpRequest();
                xhr.open('POST', $("#inpEvDes").attr('ajax-target'), true);
                xhr.setRequestHeader('X-REQUESTED-WITH', 'XMLHttpRequest')            
                xhr.onreadystatechange = async function() {
                    if(xhr.readyState == 4) {
                        if(xhr.status == 200) {
                            res = JSON.parse(xhr.responseText);
                            if(res.status == 'success') {
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
                            await swal.fire({
                                position: 'center',
                                icon: "error",
                                title: "No se pudo",
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
                    title: "No existe",
                    showConfirmButton: false,
                    timer: 3000
                })
            }
        } else {
            swal.fire({
                position: 'center',
                icon: "warning",
                title: "Debe llenar todos los campos",
                showConfirmButton: false,
                timer: 3000
            })
        }
    });

    $("#btnCerrar").click(function () {
        $("#form_subir_ev").hide();
        $("#form_subir_ev").trigger("reset");
    });

    $("select[name='sl_origen']").change(function() {
        if($(this).val() == 'N') {
            $(this).prop("selectedIndex", 0);
            $(".box").toggle();
        }
    });

    $("#checkSelect").change(function () {
        if($(this).is(":checked")) {
            $("#btn_provee").removeAttr("ajax-url");
            $(".opcion_pro_cli").text("Agregar cliente");
            $("#direccion").show();
            $("#direccion").find("textarea").attr("disabled");
            $("#btn_provee").attr("ajax-url", "/cliente_sigssmac");
        } else {
            $("#btn_provee").removeAttr("ajax-url");
            $(".opcion_pro_cli").text("Agregar proveedor");
            $("#direccion").find("textarea").removeAttr("disabled");
            $("#btn_provee").attr("ajax-url", "/proveedores/agregar_proveedores");
            $("#direccion").hide();
        }
    });

    $(".btnClose").click(async function () {
        await $(".form-box").trigger("reset");
        $(".box").toggle();
    });


    $(".form-box").submit(function (e) {
        e.preventDefault();
        var this_ = $(this);
        if(validarFormulario(".form-box")) {
            $.ajax({
                type: "POST",
                url: $("#btn_provee").attr("ajax-url"),
                data: this_.serializeArray(),
                success: async function (response) {
                    if(response.status == "success") {
                        await swal.fire({
                            position: 'center',
                            icon: response.status,
                            title: response.msg_salida,
                            showConfirmButton: false,
                            timer: 3000
                        })
                        this_.trigger("reset");
                        location.reload(true);
                    } else {
                        await swal.fire({
                            position: 'center',
                            icon: response.status,
                            title: response.msg_salida,
                            showConfirmButton: false,
                            timer: 3000
                        })
                    }
                }
            });
        } else {
            swal.fire({
                position: 'center',
                icon: "warning",
                title: "Todos los campos deben estar llenos",
                showConfirmButton: false,
                timer: 4000
            })
        }

    });
});