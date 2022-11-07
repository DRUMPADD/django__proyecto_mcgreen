let t_body = document.querySelector(".t_body");
let form = document.querySelector(".form_manteinment")
let form_update = document.querySelector(".form_update")
let box_update_form = document.getElementById("content-hidden");
let btnClose = document.querySelector(".btnClose");

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

function hideUpdateForm() {
    box_update_form.style.visibility = "hidden";
    box_update_form.style.opacity = 0;
    form_update.reset();
}

btnClose.addEventListener("click", () => {
    hideUpdateForm();
});

async function getCorMant () {
    let res = await fetch("/plataforma/correctivo/mostrarCorrectivo");
    let d = await res.json();
    return d.msg;
}


async function showCorMant () {
    let cor_mant = await getCorMant();
    let ar_cor_mant = new Array(cor_mant);
    let str_mant = "";

    ar_cor_mant[0].forEach(element => {
        if(element.length !== 0) {
            str_mant += `
                <tr>
                    <td>${element[1] != null ? element[1] : ""}</td>
                    <td>${element[2] != null ? element[2] : ""}</td>
                    <td>${element[3] != null ? element[3] : ""}</td>
                    <td>${element[4] != null ? element[4] : ""}</td>
                    <td>${element[5] != null ? element[5] : ""}</td>
                    <td>${element[6] != null ? element[6] : ""}</td>
                    <td>${element[7] != null ? element[7] : ""}</td>
                    <td>${element[8] != null ? element[8] : ""}</td>
                    <td>${element[9] != null ? element[9] : ""}</td>
                    <td>${element[10] != null ? element[10] : ""}</td>
                    <td>${element[11] != null ? element[11] : ""}</td>
                </tr>
            `
        }
    });

    t_body.innerHTML = str_mant;
}

window.addEventListener("DOMContentLoaded", () => {
    showCorMant();
})

function checkData (value_) {
    return value_ != "" && value_ != null && value_ != undefined && value_ != '--Seleccionar--';
}

function createManteinment (data_) {
    fetch("/plataforma/correctivo/agregarCorrectivo", {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(data_)
    })
    .then(res => {
        return res.json();
    })
    .then(async d => {
        await Swal.fire({
            position: 'center',
            icon: d.status,
            title: d.msg,
            confirmButtonColor: '#19ec27',
            confirmButtonText: 'ACEPTAR',
        })
        showCorMant();
        form.reset();
    })
    .catch(e => {
        Swal.fire({
            position: 'center',
            icon: "error",
            title: "Error al registrar los datos",
            confirmButtonColor: '#df1c11',
            confirmButtonText: 'ACEPTAR',
        })
    })
}

function modifyManteinment (data_) {
}

form.addEventListener("submit", (e) => {
    e.preventDefault();
    let ar = new Array();
    for(let i = 0; i < form.elements.length; i++) {
        ar.push(form.elements[i].value);
    }

    if((form["sl_item"].value != undefined || form["sl_item"].value != "")) {
        createManteinment({
            item: ar[1],
            days: ar[6],
            novedad: ar[3],
            fail: ar[2],
            report_date: ar[4],
            rec_date: ar[5],
            notes: ar[7],
        })
    } else {
        Swal.fire({
            position: 'center',
            icon: 'warning',
            title: 'Todos los campos son requeridos',
            confirmButtonColor: '#d33',
            confirmButtonText: 'ACEPTAR',
        })
    }
})

form.addEventListener("change", (e) => {
    const d1 = (new Date(form["reporte"].value).getTime())/1000/60/60/24;
    const d2 = (new Date(form["entrega"].value).getTime())/1000/60/60/24;
    if(d1 && d2) {
        form["dias"].value = d2 - d1;
    }
})

form_update.addEventListener("submit", (e) => {
    e.preventDefault();
    let ar = new Array();
    for(let i = 0; i < form_update.elements.length; i++) {
        ar.push(form_update.elements[i].value);
    }

    modifyManteinment({
        mant_id: ar[0],
        item: ar[1],
        ubicacion: ar[2],
        novedad: ar[3],
        fail: ar[4],
        report: ar[5],
        rec_date: ar[6],
        days: ar[7],
        notes: ar[8],
    })
})