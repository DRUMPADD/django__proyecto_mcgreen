$(document).ready(function() {
    $("#buscar").keyup(function (e) {
        _this = this;

        $.each($("#table tbody tr"), function () {
            if($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) !== -1) {
                $(this).show();
            } else { 
                $(this).hide();
            }
        })
        document.getElementById("buscar").addEventListener("click", function (e) {
            $(this).empty();
        })

        e.preventDefault();
    });
});