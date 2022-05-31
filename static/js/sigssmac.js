$(document).ready(function () {
    $("input[name='fecha_compromiso']").hide();
    $("#btnVolver").hide();

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
    $("form").submit(function (e) {
        e.preventDefault();
        var cont_inputs = $('input').filter(function(){
            var this_i = $(this);
            if(this_i.attr("name") != 'herramientas') {
                return this_i.val() == '';
            }
        }).length;
        var selects = $('select').filter(function(){
            var this_sl = $(this);
            if(this_sl.attr("name") != 'sl_afecta') {
                return this_sl.val() == null;
            }
        }).length;
        if(cont_inputs == 0 && $("textarea").val().trim() != '' && selects == 0 && $("input[name='hallazgos']").val() != '') {
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
});