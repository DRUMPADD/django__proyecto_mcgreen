let t_body = document.querySelector(".t_body");
let box_update_form = document.getElementById("content-hidden");
let form_mant = document.querySelector(".form-mant");
let form_update = document.querySelector(".form_update");
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

async function getGeneralManteinment () {
    let response = await fetch("/plataforma/general/mostrarGeneral");
    let data = await response.json();
    return data.msg;
}

async function showGeneralManteinment () {
    let gen_info = await getGeneralManteinment();
    let ar_gen = new Array(gen_info);
    let str_info = "";

    ar_gen[0].forEach(element => {
        if(element.length !== 0) {
            str_info += `
                <tr>
                    <td>${element[0] != null ? element[0] : ""}</td>
                    <td>${element[1] != null ? element[1] : ""}</td>
                    <td>${element[2] != null ? element[2] : ""}</td>
                    <td>${element[3] != null ? element[3] : ""}</td>
                    <td>${element[4] != null ? element[4] : ""}</td>
                    <td>${element[5] != null ? element[5] : ""}</td>
                    <td>${element[6] != null ? element[6] : ""}</td>
                    <td>${element[7] != null ? element[7] : ""}</td>
                    <td>${element[8] != null ? element[8] : ""}</td>
                    <td>${element[9] != null ? element[9] : "Sin fecha"}</td>
                    <td>${element[10] != null ? element[10] : 0}</td>
                    <td style="display: none;">${element[11] != null ? element[11] : ""}</td>
                    <td><a href="#" data-title="Ver detalles" class="details"><i class="fa-solid fa-book"></i></a></td>
                    <td><a href="#" class="btn-modificar"><i class="fa-solid fa-pencil"></i></a></td>
                    <td><a href="#" class="btn-eliminar"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>
            `;
        }
    });

    t_body.innerHTML = str_info;

    let btnsUpdate = document.querySelectorAll(".btn-modificar");
    let btnsDelete = document.querySelectorAll(".btn-eliminar");
    for(let i = 0; i < btnsUpdate.length; i++) {
        btnsUpdate[i].addEventListener("click", (e) => {
            box_update_form.style.visibility = "visible";
            box_update_form.style.opacity = 1;
            const parentTR = btnsUpdate[i].parentElement.parentElement;
            form_update["id_mant"].value = parentTR.getElementsByTagName("td")[0].innerText;
            form_update["sl_item"].value = parentTR.getElementsByTagName("td")[3].innerText;
            form_update["sl_frec"].value = parentTR.getElementsByTagName("td")[11].innerText;
            form_update["sl_act"].value = parentTR.getElementsByTagName("td")[7].innerText;
            form_update["fec-creacion"].value = parentTR.getElementsByTagName("td")[6].innerText;
            form_update["fec-proxima"].value = parentTR.getElementsByTagName("td")[9].innerText;
        });
    }
    
    for(let i = 0; i < btnsDelete.length; i++) {
        btnsDelete[i].addEventListener("click", (e) => {
            const parentTR = btnsUpdate[i].parentElement.parentElement;
            Swal.fire({
                title: "¿Está seguro de eliminar este registro?",
                text: "Esta acción no podrá ser revertida",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, eliminar',
                cancelButtonText: 'Cancelar',
            }).then(result => {
                if(result.isConfirmed) {
                    deleteManteinment(parentTR.getElementsByTagName("td")[0].innerText)
                }
            })
        });
    }
}


window.addEventListener("DOMContentLoaded", () => {
    showGeneralManteinment();
})

function createManteinment (elements) {
    fetch("/plataforma/general/crearGeneral", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie("csrftoken")
        },
        body: JSON.stringify(elements)
    })
    .then(res => {
        return res.json();
    })
    .then(async d => {
        Swal.fire({
            position: 'center',
            icon: d.status,
            title: d.msg,
            confirmButtonColor: '#19ec27',
            confirmButtonText: 'ACEPTAR',
        })
        showGeneralManteinment()
        form_mant.reset();
    })
    .catch(err => {
        Swal.fire({
            position: 'center',
            icon: "error",
            title: "Error al registrar los datos",
            confirmButtonColor: '#df1c11',
            confirmButtonText: 'ACEPTAR',
        })
    })
}

function checkInput(value_inp) {
    return value_inp != null && value_inp != undefined && value_inp != "" && value_inp != '--Seleccionar--';
}

function modifyManteinment (answers) {
    fetch("/plataforma/general/modificarGeneral", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie("csrftoken")
        },
        body: JSON.stringify(answers)
    })
    .then(res => {
        return res.json();
    })
    .then(async d => {
        Swal.fire({
            position: 'center',
            icon: d.status,
            title: d.msg,
            confirmButtonColor: '#19ec27',
            confirmButtonText: 'ACEPTAR',
        })
        showGeneralManteinment()
        hideUpdateForm();
    })
    .catch(err => {
        Swal.fire({
            position: 'center',
            icon: "error",
            title: "Error al modificar los datos",
            confirmButtonColor: '#df1c11',
            confirmButtonText: 'ACEPTAR',
        })
    })
}

function deleteManteinment (mant_id) {
    fetch("/plataforma/general/eliminarGeneral", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie("csrftoken")
        },
        body: JSON.stringify({
            prev_id: mant_id
        })
    })
    .then(response => {
        return response.json();
    })
    .then(d => {
        Swal.fire({
            position: 'center',
            icon: d.status,
            title: d.msg,
            confirmButtonColor: '#19ec27',
            confirmButtonText: 'ACEPTAR',
        })
        showGeneralManteinment()
    })
    .catch(err => {
        Swal.fire({
            position: 'center',
            icon: "error",
            title: "Error al eliminar registro",
            confirmButtonColor: '#df1c11',
            confirmButtonText: 'ACEPTAR',
        })
    })
}

form_mant.addEventListener("submit", (e) => {
    e.preventDefault();
    let arr_els = new Array();
    for(let i = 0; i < form_mant.elements.length; i++) {
        arr_els.push(form_mant.elements[i].value);
    }

    let validForm = checkInput(arr_els[0]) && checkInput(arr_els[1]) && checkInput(arr_els[2]) && checkInput(arr_els[3]) && checkInput(arr_els[4]);

    if(validForm) {
        createManteinment(
            { 
                item_id: arr_els[0], 
                frec_: arr_els[1], 
                act_: arr_els[2], 
                create_date: arr_els[3], 
                date_next: arr_els[4],
            }
        );
    } else {
        Swal.fire({
            position: 'center',
            icon: "warning",
            title: "Todos los campos son requeridos",
            confirmButtonColor: '#df1c11',
            confirmButtonText: 'ACEPTAR',
        })
    }
})

form_update.addEventListener("submit", (e) => {
    e.preventDefault();
    let arr_els = new Array(), full = 0;
    for(let i = 0; i < form_update.elements.length - 1; i++) {
        arr_els.push(form_update.elements[i].value);
        full = checkInput(form_update.elements[i].value) ? full++ : full;
    }

    modifyManteinment({
        item_id: arr_els[2],
        frec_: arr_els[3],
        create_date: arr_els[5],
        act_: arr_els[4],
        date_next: arr_els[6],
        prev_cod: arr_els[1],
    })
})