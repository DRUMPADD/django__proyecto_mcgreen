$(document).ready(function () {
    $(".ver_img").each(function(index) {
        var $this_ = $(this);
        $this_.click(function () {
            var div_display = $("#display_i");
            var img_src = $("#img_mostrar");
            img_src.attr("src", $this_.attr("src-img"));
            img_src.show();
            div_display.css("display", "block");
        });
    });
    $("form").submit(function (e) {
        e.preventDefault();
        var cont_inputs = $('input').filter(function(){return $(this).val() == ''}).length;
        if(cont_inputs == 0 && $("textarea").val().trim() != '' && $("input[name='hallazgos']").val() != '') {
            if(window.FormData !== undefined) {
                var formData = new FormData(this);
                var xhr = new XMLHttpRequest();
                xhr.open('POST', $("#enviar_sigssmac").attr('ajax'), true);
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
                                await $("form").trigger("reset");
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
                            swal.fire({
                                position: 'center',
                                icon: "error",
                                title: "Error al enviar la información",
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
                    title: "La información no pudo ser enviada",
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
});