const indices_ = document.getElementById("indices_");
const canvas_ = document.getElementById("datos_accidentabilidad");
const tbody_det = document.querySelector(".tbody_det");
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
        ar_.push(res_[i][4]);
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
        plugins: [ChartDataLabels],
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    
                },
            },
            distribution: 'linear',
            responsive: true,
            legend: {
                display: true,
                labels: {
                    fontFamily: "'Arial', 'sans-serif'",
                    fontSize: 20
                },
            },
            plugins: {
                datalabels: {
                    labels: {
                        title: {
                            font: {
                                weight: 'bold',
                                size: 13
                            }
                        },
                    },
                    anchor: 'end',
                    align: 'top'
                }
            }
        },
    })
}

async function mostrar_datos2() {
    let d_ = await obtener_datos();
    let res_ = d_.respuesta;

    for(let i = 0; i < res_.length; i++) {
        tbody_det.innerHTML += `
            <tr>
                <td>${res_[i][0]}</td>
                <td>${res_[i][1]}</td>
                <td>${res_[i][2]}</td>
                <td>${res_[i][3]}</td>
                <td>${res_[i][4]}</td>
                <td>${res_[i][3] / res_[i][5]}</td>
                <td>${res_[i][2] / (res_[i][5] * 1000000)}</td>
            </tr>
        `;
    }
}

async function mostrar_datos3() {
    let cont = new Array();
    let d_ = await obtener_datos();
    let res_ = d_.respuesta;
    var ar_frecuencia = new Array();
    var ar_gravedad = new Array();
    var cont_datos = res_.length;
    var max_frecuencia = 0, max_gravedad = 0;
    for(let i = 0; i < cont_datos; i++) {
        var cal_frec = res_[i][3] / res_[i][5];
        var cal_grav = res_[i][2] / (res_[i][5] * 1000000);
        if(cal_frec >= cal_grav) {
            max_frecuencia = cal_frec;
        } else {
            max_gravedad = cal_grav;
        }
        ar_frecuencia.push(res_[i][3] / res_[i][5]);
        ar_gravedad.push(res_[i][2] / (res_[i][5] * 1000000));
    }

    console.log(max_frecuencia);
    console.log(max_gravedad);

    for(let i = 0; i < cont_datos; i++) {
        cont.push(res_[i][0]);
    }

    new Chart(indices_, {
        type: 'line',
        data: {
            labels: cont,
            datasets: [
                {
                    label: "Índices de frecuencia",
                    data: ar_frecuencia,
                    borderWidth: 3,
                    borderColor: 'rgb(4, 28, 190)'
                },
                {
                    label: "Índices de gravedad",
                    data: ar_gravedad,
                    borderWidth: 3,
                    borderColor: 'rgb(186, 28, 38)'
                },
            ]
        },
        plugins: [ChartDataLabels],
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: max_frecuencia >= max_gravedad ? max_frecuencia : max_gravedad
                },
            },
            distribution: 'linear',
            responsive: true,
            legend: {
                display: true,
                labels: {
                    fontFamily: "'Arial', 'sans-serif'",
                    fontSize: 20
                },
            },
            plugins: {
                datalabels: {
                    labels: {
                        title: {
                            font: {
                                weight: 'bold',
                                size: 13
                            }
                        },
                    },
                    anchor: 'end',
                    align: 'top'
                }
            }
        },
    })
}

window.addEventListener("DOMContentLoaded", () => {
    mostrar_datos();
    mostrar_datos2();
    mostrar_datos3();
})

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
        swal.fire({
            position: 'center',
            icon: "error",
            title: "Ocurrió un error en el sistema",
            showConfirmButton: false,
            timer: 3000
        });
    })
}


function validar_personal_propio() {
    return form_registro["c_personal"][0].value && form_registro["h_trabajo"][0].value && form_registro["jornada"][0].value && form_registro["acci_c_baja"][0].value && form_registro["dias_inc"][0].value;
}

function validar_personal_contratado() {
    return form_registro["c_personal"][1].value && form_registro["h_trabajo"][1].value && form_registro["jornada"][1].value && form_registro["acci_c_baja"][1].value && form_registro["dias_inc"][1].value;
}

form_registro.addEventListener("submit", (e) => {
    e.preventDefault();
    if(form_registro["anio"].value && form_registro["sl_mes"].value) {
        if((validar_personal_propio() || validar_personal_contratado())) {
            enviar_registro({
                "c_personal": [form_registro["c_personal"][0].value, form_registro["c_personal"][1].value],
                "h_trabajo": [form_registro["h_trabajo"][0].value, form_registro["h_trabajo"][1].value],
                "jornada": [form_registro["jornada"][0].value, form_registro["jornada"][1].value],
                "mes": form_registro["sl_mes"].value != undefined || form_registro["sl_mes"].value != null ? form_registro["sl_mes"].value : '',
                "anio": form_registro["anio"].value != '' ? form_registro["anio"].value : '',
                "acci_c_baja": [form_registro["acci_c_baja"][0].value, form_registro["acci_c_baja"][1].value],
                "dias_inc": [form_registro["dias_inc"][0].value, form_registro["dias_inc"][1].value],
            });
    
            form_registro.reset();
        } else {
            swal.fire({
                position: 'center',
                icon: 'warning',
                title: 'Debe llenar al menos una de las 2 categorías',
                showConfirmButton: false,
                timer: 6000
            })
        }
    } else {
        swal.fire({
            position: 'center',
            icon: 'warning',
            title: 'Debe elegir mes y año',
            showConfirmButton: false,
            timer: 6000
        })
    }
})