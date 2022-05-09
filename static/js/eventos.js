$(document).ready(function() {
    $("#buscar_evt").keyup(function (e) {
        _this = this;

        $.each($("#t_evt tbody tr"), function () {
            if($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) !== -1) {
                $(this).show();
            } else { 
                $(this).hide();
            }
        })
        document.getElementById("buscar_evt").addEventListener("click", function (e) {
            $(this).empty();
        })

        e.preventDefault();
    });
    
    $("#buscar_act").keyup(function (e) {
        _this = this;

        $.each($("#t_act tbody tr"), function () {
            if($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) !== -1) {
                $(this).show();
            } else { 
                $(this).hide();
            }
        })
        document.getElementById("buscar_act").addEventListener("click", function (e) {
            $(this).empty();
        })

        e.preventDefault();
    });
});