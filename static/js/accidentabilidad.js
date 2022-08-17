const form_registro = document.querySelector(".form-registro");

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function enviar_registro(datos) {
    fetch("/registrar_acci", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
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
    return form_registro["c_personal"][0].value != '' && form_registro["h_trabajo"][0].value != '' && form_registro["jornada"][0].value != '';
}

function validar_personal_contratado() {
    return form_registro["c_personal"][1].value != '' && form_registro["h_trabajo"][1].value != '' && form_registro["jornada"][1].value != '';
}

form_registro.addEventListener("submit", (e) => {
    e.preventDefault();
    console.log((validar_personal_propio() || validar_personal_contratado()) && (form_registro["anio"].value != '' && form_registro["sl_mes"].value != null));
    if((validar_personal_propio() || validar_personal_contratado()) && (form_registro["anio"].value != '' && form_registro["sl_mes"].value != null)) {
        enviar_registro({
            "c_personal": [form_registro["c_personal"][0].value, form_registro["c_personal"][1].value],
            "h_trabajo": [form_registro["h_trabajo"][0].value, form_registro["h_trabajo"][1].value],
            "jornada": [form_registro["jornada"][0].value, form_registro["jornada"][1].value],
            "mes": form_registro["sl_mes"].value != undefined || form_registro["sl_mes"].value != null ? form_registro["sl_mes"].value : '',
            "anio": form_registro["anio"].value != '' ? form_registro["anio"].value : '',
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

async function obtener_datos() {
    let datos = await fetch("/datos_generales_obtenidos");
    let res = await datos.json();
    return res;
}




async function mostrar_datos() {
    let cont = new Array();
    let d_ = await obtener_datos();
    let res_ = d_.respuesta;
    var ar_ = new Array();
    var cont_datos = res_.length;
    for(let i = 0; i < cont_datos; i++) {
        ar_.push(res_[i][2]);
    }

    for(let i = 0; i < cont_datos; i++) {
        cont.push(res_[i][0]);
    }

    new Chart(canvas_, {
        type: 'line',
        data: {
            labels: cont,
            datasets: [
                {
                    label: "Empleados por mes",
                    data: ar_,
                    borderWidth: 3,
                    borderColor: 'rgba(0, 0, 0, 0.9)'
                }
            ]
        },
        options: {
            chartArea: {
                backgroundColor: 'rgba(0, 0, 0, 0.7)'
            }
        }
    })
}



const canvas_ = document.getElementById("datos_accidentabilidad");

window.addEventListener("DOMContentLoaded", () => {
    mostrar_datos();
})