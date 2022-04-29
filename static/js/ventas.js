$(document).ready(function () {
    $("#form-c_p_c select[name='sl_sistemas']").on('change', function() {
        var precio = $(this).val().split(' ')[2];
        var medida = $(this).val().split(' ')[1];
        
        $("input[name='precio']").val(parseFloat(precio));
        $("input[name='medida']").val(medida);
    });

    $("form").submit(function (e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: $("#btn_venta").attr("target-ajax"),
            data: $("form").serializeArray(),
            success: function(response) {
                switch(response.status) {
                    case 'success':
                        swal.fire({
                            position: 'center',
                            icon: response.status,
                            title: response.mensaje,
                            showConfirmButton: false,
                            timer: 4000
                        })
                        $("form").trigger("reset");
                        break;
                    default:
                        swal.fire({
                            position: 'center',
                            icon: response.status,
                            title: response.mensaje,
                            showConfirmButton: false,
                            timer: 4000
                        })
                        break;
                }
            }
        });
    });
});