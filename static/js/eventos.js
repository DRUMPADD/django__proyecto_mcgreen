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

    $("form").each(function(index) {
        var this_ = $(this);
        this_.submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: "POST",
                url: $("button").attr("target"),
                data: this_.serializeArray(),
                success: async function (res) {
                    if(res.status == 'success') {
                        await swal.fire({
                            position: 'center',
                            icon: res.status,
                            title: res.msg,
                            showConfirmButton: false,
                            timer: 2000
                        })
                        location.reload(true);
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
});