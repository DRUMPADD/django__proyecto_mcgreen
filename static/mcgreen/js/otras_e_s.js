$(document).ready(function () {

    function validar_formulario() {
        var valido = false, valido_s = false;
        $("form input").each(function () {
            if($(this).val === '') {
                valido = true;
            }
        })
        $("form select option:selected").change(function () {
            if($(this).is('disabled')) {
                valido_s = true;
            }
        })

        return valido && valido_s;
    }

    $("select[name='sl_productos']").change(function() {
        $("input[name='medida']").val($(this).val().split(' ')[1]);
    });

    $("form").submit(function (e) {
        e.preventDefault();
        
        if(validar_formulario() === false) {
            $.ajax({
                type: 'POST',
                url: $("#btn_enviar").attr("target-ajax"),
                data: $("form").serializeArray(),
                success: function (res) {
                    switch(res.status) {
                        case 'success':
                            $("form").trigger("reset");
                            swal.fire({
                                position: 'center',
                                icon: res.status,
                                title: res.mensaje,
                                showConfirmButton: false,
                                timer: 2000
                            })
                            break;
                        default:
                            swal.fire({
                                position: 'center',
                                icon: res.status,
                                title: res.mensaje,
                                showConfirmButton: false,
                                timer: 2000
                            })
                            break;
                    }
                }
            });
        } else {
            swal.fire({
                position: 'center',
                icon: 'warning',
                title: 'Debe llenar todos los campos',
                showConfirmButton: false,
                timer: 2000
            })
        }
    });
});