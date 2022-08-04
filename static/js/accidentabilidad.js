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
    return form_registro["c_personal"][0].value != null && form_registro["h_trabajo"][0].value != null && form_registro["jornada"][0].value != null;
}

function validar_personal_contratado() {
    return form_registro["c_personal"][1].value != null && form_registro["h_trabajo"][1].value != null && form_registro["jornada"][1].value != null;
}

form_registro.addEventListener("submit", (e) => {
    e.preventDefault();
    console.log(validar_personal_propio() || validar_personal_contratado());
    if(validar_personal_propio() || validar_personal_contratado()) {
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


async function obtener_datos_con() {
    let datos = await fetch("/accidentabilidad_contratados");
    let res = await datos.json();
    return res;
}
async function obtener_datos_pro() {
    let datos = await fetch("/accidentabilidad_propios");
    let res = await datos.json();
    return res;
}




async function mostrar_datos() {
    let cont = new Array();
    let d_con = await obtener_datos_con();
    let d_pro = await obtener_datos_pro();
    let res_c = d_con.contratados;
    let res_p = d_pro.propios;
    var ar_c = new Array();
    var ar_p = new Array();
    var cont_datos = 0;
    if(res_c.length > res_p.length) {
        cont_datos = res_c.length;
    } else {
        cont_datos = res_p.length;
    }

    for(let i = 0; i < cont_datos; i++) {
        if(res_c[i][0]) {
            ar_c.push(res_c[i][0]);
            console.log(res_c[i][0]);
        } else {
            ar_c.push(0);
        }
    }
    for(let i = 0; i < cont_datos; i++) {
        if(res_p[i][0]) {
            ar_p.push(res_p[i][0]);
            console.log(res_p[i][0]);
        } else {
            ar_p.push(0);
        }
    }
    console.log(ar_c);
    console.log(ar_p);

    for(let i = 0; i < cont_datos; i++) {
        cont.push(i+1);
    }

    

    let contratados = {
        label: "Contratados",
        data: ar_c,
        backgroundColor: 'rgba(218, 202, 58, .4)', // Color de fondo
        borderColor: 'rgba(218, 202, 58, 1)',
        borderWidth: 3,
        tension: .5,
        fill: true,
    };
    
    let propios = {
        label: "Propios",
        data: ar_p,
        backgroundColor: 'rgba(22, 170, 133, .4)',
        borderColor: 'rgba(22, 170, 133, 1)',
        borderWidth: 3,
        tension: .5,
        fill: true,
    };

    new Chart(canvas_, {
        type: 'line',
        data: {
            labels: cont,
            datasets: [
                contratados,
                propios,
            ]
        }
    })
}



const canvas_ = document.getElementById("datos_accidentabilidad");

window.addEventListener("DOMContentLoaded", () => {
    mostrar_datos();
})