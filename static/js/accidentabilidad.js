const form_registro = document.querySelector(".form-registro");

function enviar_registro(datos) {
    fetch("/registrar_acci", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(datos)
    })
    .then(res => {
        return res.json();
    })
    .then(async (data) => {
        console.log(data.res);
        await swal.fire({
            position: 'center',
            icon: data.status,
            title: data.res,
            showConfirmButton: false,
            timer: 3000
        })
        location.reload();
    })
    .catch(err => {
        console.log(err);
    })
}


function validar_personal_propio() {
    return form_registro["c_personal"][0].value != null && form_registro["h_trabajo"][0].value != null && form_registro["jornada"][0].value != null;
}

function validar_personal_contratado() {
    return form_registro["c_personal"][1].value != null && form_registro["h_trabajo"][1].value != null && form_registro["jornada"][1].value != null;
}

form_registro.addEventListener("submit", (e) => {
    e.preventDefault();

    if(validar_personal_propio || validar_personal_contratado) {
        enviar_registro({
            "c_personal": [form_registro["c_personal"][0].value, form_registro["c_personal"][1].value],
            "h_trabajo": [form_registro["h_trabajo"][0].value, form_registro["h_trabajo"][1].value],
            "jornada": [form_registro["jornada"][0].value, form_registro["jornada"][1].value],
        });

        form_registro.reset();
    } else {
        swal.fire({
            position: 'center',
            icon: 'warning',
            title: 'Debe llenar al menos uno de los dos formularios',
            showConfirmButton: false,
            timer: 6000
        })
    }
})