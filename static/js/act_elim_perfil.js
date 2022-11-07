$(document).ready(function () {
    var vacante_act = $("input[name='vacante']").val();
    $("#agregar_v").click(function () {
        $("input[name='vacante']").val(++vacante_act);
    });
    $("#quitar_v").click(function () {
        $("input[name='vacante']").val(--vacante_act);
    });

    if (vacante_act != vacante_act) {
        $("#actualizar_v").removeAttr("hidden");
    }

    $("#actualizar_perfil").hide();
    
    $(".btn_perfil").each(function () {
        $(this).click(function () {
            $("#actualizar_perfil").fadeToggle();
            var panorama_btn = $(this).parent().parent();
            $("input[name='opcion']").val("MODIFICAR PAP");
            $("input[name='formacion']").val($(panorama_btn).find("td").eq(0).text());
            $("input[name='escolaridad']").val($(panorama_btn).find("td").eq(1).text());
            $("input[name='perfil_p']").val($(panorama_btn).find("td").eq(2).text());
            $("input[name='experiencia']").val($(panorama_btn).find("td").eq(3).text());
            $("input[name='nombre_puesto']").val();
            $("input[name='objetivo']").val();
            $("#nombre_p").hide();
            $("#objetivo").hide();
            $("#formacion").show();
            $("#escolaridad").show();
            $("#perfil_p").show();
            $("#experiencia").show();
            if($("#actualizar").attr("dato-ajax")) {
                $("#actualizar").removeAttr("dato-ajax");
                $("#actualizar").attr("dato-ajax", "/actualizar_perfil");
            }
        });
    });
    
    $("#btn_generalidades").click(function () {
        $("#actualizar_perfil").fadeToggle();
        var panorama_btn = $(this).parent().parent();
        $("input[name='opcion']").val("MODIFICAR GEN");
        $("input[name='formacion']").val();
        $("input[name='escolaridad']").val();
        $("input[name='perfil_p']").val();
        $("input[name='experiencia']").val();
        $("#formacion").hide();
        $("#escolaridad").hide();
        $("#perfil_p").hide();
        $("#experiencia").hide();
        $("#nombre_p").show();
        $("#objetivo").show();
        $("input[name='nombre_puesto']").val($(panorama_btn).find("td").eq(0).text());
        $("input[name='objetivo']").val($(panorama_btn).find("td").eq(4).text());
        if($("#actualizar").attr("dato-ajax")) {
            $("#actualizar").removeAttr("dato-ajax");
            $("#actualizar").attr("dato-ajax", "/actualizar_gen");
        }
    });

    $("#actualizar_perfil").submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: $("#actualizar").attr("dato-ajax"),
            data: $("#actualizar_perfil").serializeArray(),
            success: function (res) {
                switch(res.status) {
                    case 'success':
                        $("#actualizar_perfil").trigger("reset");
                        $("#actualizar_perfil").hide();
                        swal(res.msg, res.msg_salida, res.status);
                        break;
                    case 'error':
                        swal(res.msg, res.msg_salida, res.status);
                        break;
                }
            },
            error: function () {
                swal("Error", "Los datos no pudieron ser enviados", "error");
            }
        });
    });


    $(".formulario_sub").each(function () {
        var $this = $(this);
        $this.submit(function (e) {
            $.ajax({
                type: "POST",
                url: $(".btn_eliminar_sub").attr("dato-ajax"),
                data: $this.serializeArray(),
                success: function (res) {
                    swal(res.msg, res.msg_salida, res.status);
                }
            });
            $.ajax({
                type: "GET",
                url: $("#mostrar_info").attr("regresar"),  // URL to your view that serves new info
                data: {'append_increment': append_increment}
            })
            .done(function(response) {
                $('#jer_sub').append(response);
            });
            e.preventDefault();
        });
    });
    $(".formulario_sup").each(function () {
        var $this = $(this);
        $this.submit(function (e) {
            $.ajax({
                type: "POST",
                url: $(".btn_eliminar_sup").attr("dato-ajax"),
                data: $this.serializeArray(),
                success: function (res) {
                    swal(res.msg, res.msg_salida, res.status);
                }
            });
            $.ajax({
                type: 'GET',
                url: $("#mostrar_info").attr("regresar")
            });
            e.preventDefault();
        });
    });
    $(".formulario_funcion").each(function () {
        var $this = $(this);
        $this.submit(function (e) {

            e.preventDefault();
            $.ajax({
                type: "POST",
                url: $(".btn_eliminar_func").attr("dato-ajax"),
                data: $this.serializeArray(),
                success: function (res) {
                    swal(res.msg, res.msg_salida, res.status);
                }
            });
            
        });
    });
    $(".formulario_resad").each(function () {
        var $this = $(this);
        $this.submit(function (e) {

            e.preventDefault();
            $.ajax({
                type: "POST",
                url: $(".btn_eliminar_resad").attr("dato-ajax"),
                data: $this.serializeArray(),
                success: function (res) {
                    swal(res.msg, res.msg_salida, res.status);
                }
            });
            
        });
    });
    $(".formulario_compg").each(function () {
        var $this = $(this);
        $this.submit(function (e) {

            e.preventDefault();
            $.ajax({
                type: "POST",
                url: $(".btn_eliminar_compg").attr("dato-ajax"),
                data: $this.serializeArray(),
                success: function (res) {
                    swal(res.msg, res.msg_salida, res.status);
                }
            });
            
        });
    });
    $(".formulario_compt").each(function () {
        var $this = $(this);
        $this.submit(function (e) {

            e.preventDefault();
            $.ajax({
                type: "POST",
                url: $(".btn_eliminar_compt").attr("dato-ajax"),
                data: $this.serializeArray(),
                success: function (res) {
                    swal(res.msg, res.msg_salida, res.status);
                }
            });
            
        });
    });
    $(".formulario_aspss").each(function () {
        var $this = $(this);
        $this.submit(function (e) {

            e.preventDefault();
            $.ajax({
                type: "POST",
                url: $(".btn_eliminar_aspss").attr("dato-ajax"),
                data: $this.serializeArray(),
                success: function (res) {
                    swal(res.msg, res.msg_salida, res.status);
                }
            });
            
        });
    });
    $(".formulario_reqfis").each(function () {
        var $this = $(this);
        $this.submit(function (e) {

            e.preventDefault();
            $.ajax({
                type: "POST",
                url: $(".btn_eliminar_reqfis").attr("dato-ajax"),
                data: $this.serializeArray(),
                success: function (res) {
                    swal(res.msg, res.msg_salida, res.status);
                }
            });
            
        });
    });
});