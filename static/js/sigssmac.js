$(document).ready(function () {
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
                                title: "Error al enviar la información",
                                showConfirmButton: false,
                                timer: 3000
                            })
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
});