$(document).ready(function() {
    $('.producto').on('click', (e) => {
        const element = $(this)[0].activeElement.parentElement.parentElement;
        // console.log($(element).find("td").eq(5).text());
        const precio = parseFloat($(element).find("td").eq(5).text().split(" ")[1].replace(',', ''));
        // console.log(precio);
        $("input[name='id_producto']").val($(element).find("th").text());
        $("input[name='producto']").val($(element).find("td").eq(0).text());
        $("input[name='descripcion']").val($(element).find("td").eq(1).text());
        $("input[name='precio']").val(precio);
        $("#BtnGuardar").val("Modificar").addClass("btn-success");
        $("#BtnGuardar").removeClass("btn-primary");
        if(!document.getElementById('cancelar')) {
            // $("#form-pro div:last").append(
            //     $(document.createElement('input')).prop({
            //         type: 'button',
            //         value: 'Cancelar',
            //         class: 'btn btn-danger form-control',
            //         name: 'btncancelar',
            //         id: 'cancelar'
            //     })
            // );
            $(this).val("Cancelar");
            $("#form-pro").attr('action', "modificar_producto");
        }

        e.preventDefault();
    });
});