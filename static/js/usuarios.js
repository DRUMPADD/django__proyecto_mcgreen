$(document).ready(function() {
    $("input[name='actualizar']").on('click', function () {
        $(this).each(function () {
            let formulario = $(this)[0].activeElement.parentElement.parentElement;
            console.log($(formulario).find(":input").eq(0).val());
            console.log($(formulario).find(":input").eq(1).val());
            console.log($(formulario).find(":input").eq(2).val());
            console.log($(formulario).find(":input").eq(3).val());
            console.log($(formulario).find(":input").eq(4).val());
            console.log($(formulario).find(":input").eq(5).val());
            console.log($(formulario).find(":input").eq(6).val());
            $(formulario).find(":input").eq(0).removeAttr("readonly");
            $(formulario).find(":input").eq(1).removeAttr("readonly");
            $(formulario).find(":input").eq(2).removeAttr("readonly");
            $(formulario).find(":input").eq(3).removeAttr("readonly");
            $(formulario).find(":input").eq(4).removeAttr("readonly");
            $(formulario).find(":input").eq(5).removeAttr("readonly");
            $(formulario).find(":input").eq(6).removeAttr("readonly");
            $(formulario).find(":input").eq(6).removeAttr("name");
            $(formulario).find(":input").eq(6).attr("name", "cancelar");
            $(formulario).find(":input").eq(6).val("Cancelar");
            console.log($(formulario).find(":input").eq(6).val());
        });
    });
});