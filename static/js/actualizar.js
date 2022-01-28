$(document).ready(function() {
    $("#form-actualizar").hide();

    $(".modificar_venta").on('click', (e) => {
        const element = $(this)[0].activeElement.parentElement.parentElement;
        // $(this).addClass("clicked");
        $("#form-actualizar").show();

        $("#caja_mensaje").hide();
        

        $("input[name='id_']").val($(element).find("td").eq(0).text());
        $("input[name='status']").val($(element).find("td").eq(1).text());
        $("input[name='fecha_pago_fac']").val($(element).find("td").eq(2).text());
        $("input[name='contrarecibo']").val($(element).find("td").eq(3).text());
        $("input[name='fecha_rec_pago']").val($(element).find("td").eq(4).text());
        $("input[name='fecha_de_fac']").val($(element).find("td").eq(18).text());
        $("input[name='recibo_pago_fac_mcgreen']").val($(element).find("td").eq(19).text());
        $("input[name='fecha_r_pag']").val($(element).find("td").eq(20).text());
        $("input[name='monto_mn_pagado']").val(parseFloat($(element).find("td").eq(23).text().split(" ")[1].replace(',', '')));
        e.preventDefault();
    });

    $("#closebtn").on('click', function () {
        $("#form-actualizar").trigger("reset");
        $("#form-actualizar").hide();
    });
});