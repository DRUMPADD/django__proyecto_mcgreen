$(document).ready(function () {
    $("#vista_mod").hide();
    $("#vista_agregar").hide();

    $(".modificar").each(function() {
        var $this = $(this);
        $(this).click(function() {
            var elemento = $this.parent().parent();
            $("#vista_mod").show();
            $("#vista_agregar").hide();
            $("input[name='id_mant']").val(elemento.find("td").eq(0).text());
            $("select[name='sl_nuevo_estado']").val(elemento.find("td").eq(6).text());
        });
    });

    $("#btn_cerrar").click(function() {
        $("#vista_mod").hide();
        $("#modificar_mant").trigger("reset");
    });

    $("#agregar_mant").submit((e) => {
        e.preventDefault();
        var no_vacios = $(".s").filter(function() {return $(this).val() != ''}).length;
        if($("input:empty").length != 0 && no_vacios != 0) {
            $.ajax({
                type: 'POST',
                url: $("#btn_enviar").attr("ajax-target"),
                data: $("#agregar_mant").serializeArray(),
                success: function(res) {
                    if(res.status == 'success') {
                        swal.fire({
                            position: 'center',
                            icon: res.status,
                            title: res.msg,
                            showConfirmButton: false,
                            timer: 2000
                        })
                        $("#agregar_mant").trigger("reset");
                    } else {
                        swal.fire({
                            position: 'center',
                            icon: res.status,
                            title: res.msg,
                            showConfirmButton: false,
                            timer: 2000
                        })
                    }
                }
            });
        } else {
            swal.fire({
                position: 'center',
                icon: "warning",
                title: "Debe llenar todos los campos",
                timer: 5000
            });
        }
    });

    $("#modificar_mant").submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $("#btn_mod").attr("ajax-target"),
            data: $("#modificar_mant").serializeArray(),
            success: function(res) {
                if(res.status == 'success') {
                    swal.fire({
                        position: 'center',
                        icon: res.status,
                        title: res.msg,
                        showConfirmButton: false,
                        timer: 2000
                    })
                    $("#modificar_mant").trigger("reset");
                    $("#vista_mod").hide();
                    $("#vista_agregar").show();
                } else {
                    swal.fire({
                        position: 'center',
                        icon: res.status,
                        title: res.msg,
                        showConfirmButton: false,
                        timer: 2000
                    })
                }
            }
        });
    });
});