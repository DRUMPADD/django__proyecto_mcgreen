let box_update_form = document.getElementById("content-hidden");
let form_update = document.querySelector(".form_update");
let btnClose = document.querySelector(".btnClose");
let t_body = document.getElementById("items");
let form = document.querySelector("#form_item");


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

async function getItems() {
    let response = await fetch("/plataforma/equipo/mostrarItems");
    let data = await response.json();
    return data.msg;
}

async function showItems() {
    let items = await getItems();
    let ar_items = new Array(items);
    let str_items = "";

    ar_items[0].forEach(element => {
        if(element.length !== 0) {
            str_items += `
                <tr>
                    <td>${element[0]}</td>
                    <td>${element[1]}</td>
                    <td>${element[2]}</td>
                    <td style="display: flex; justify-content: center;">
                        <a data-title="Ver características" href="/plataforma/equipo/info_item/${element[0]}" class="btn btn-see-charac">
                            <i class="fa-regular fa-file-lines"></i>
                        </a>
                        <a class="btn btn-modificar" href="#content-hidden">
                            <i class="fa-solid fa-pencil"></i>
                        </a>
                        <a class="btn btn-eliminar" href="#content-hidden">
                            <i class="fa-solid fa-trash-can"></i>
                        </a>
                    </td>
                </tr>
            `;
        }
    });

    t_body.innerHTML = str_items;
    let btns_update = document.querySelectorAll(".btn-modificar");
    let btns_delete = document.querySelectorAll(".btn-eliminar");
    for(let i = 0; i < btns_update.length; i++) {
        btns_update[i].addEventListener("click", (e) => {
            box_update_form.style.visibility = "visible";
            box_update_form.style.opacity = 1;
            const parentTR = btns_update[i].parentElement.parentElement;
            form_update["id_"].value = parentTR.getElementsByTagName("td")[0].innerText;
            form_update["new_name"].value = parentTR.getElementsByTagName("td")[1].innerText;
            form_update["new_stuck"].value = parentTR.getElementsByTagName("td")[2].innerText;
        });
    }
    for(let i = 0; i < btns_delete.length; i++) {
        btns_delete[i].addEventListener("click", (e) => {
            const parentTR = btns_delete[i].parentElement.parentElement;
            searchItem(parentTR.getElementsByTagName("td")[0].innerText);
        });
    }
}

window.addEventListener("DOMContentLoaded", () => {
    showItems();
})

function checkInput(inputId) {
    return inputId != "" && inputId != undefined && inputId != null;
}

function createItem (cod_item, name_item, quantity_item) {
    fetch("/plataforma/equipo/registrarItem", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            cod_: cod_item,
            name_: name_item,
            quantity: quantity_item
        })
    })
    .then(response => {
        return response.json();
    })
    .then(async data => {
        await Swal.fire({
            position: 'center',
            icon: data.status,
            title: data.msg,
            confirmButtonColor: '#19ec27',
            confirmButtonText: 'ACEPTAR',
        })
        showItems();
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

function modifyItem () {
    fetch("/plataforma/equipo/modificarItem", {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            id_: form_update["id_"].value,
            new_name: form_update["new_name"].value,
            new_stuck: form_update["new_stuck"].value,
        })
    })
    .then(response => {
        return response.json();
    })
    .then(async data => {
        await Swal.fire({
            position: 'center',
            icon: data.status,
            title: data.msg,
            confirmButtonColor: '#19ec27',
            confirmButtonText: 'ACEPTAR',
        })
        showItems();
        hideUpdateForm();
    })
    .catch(e => {
        Swal.fire({
            position: 'center',
            icon: "error",
            title: "Error al modificar los datos",
            confirmButtonColor: '#df1c11',
            confirmButtonText: 'ACEPTAR',
        })
    })
}


function searchItem (item_id) {
    fetch("/plataforma/equipo/buscarItem", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            cod_item: item_id
        })
    })
    .then(response => {
        return response.json();
    })
    .then(d => {
        deleteItem(d.msg, item_id);
        return d.msg;
    })
    .catch(e => {
        Swal.fire({
            position: 'center',
            icon: "error",
            title: "Error al buscar actividad",
            confirmButtonColor: '#df1c11',
            confirmButtonText: 'ACEPTAR',
        })
    })
}

function deleteItem (msg, item_id) {
    let url_fetch = msg == "Encontrados" || msg == "Encontrado" ? "/plataforma/equipo/eliminarItemCompleto" : "/plataforma/equipo/eliminarItem";
    let confirm_message = msg == "Encontrados" || msg == "Encontrado" ? "Este equipo está asignado a uno o varios registros, ¿está seguro de eliminarlo?" : "¿Está seguro de eliminar este equipo?";
    Swal.fire({
        title: confirm_message,
        text: "Esta acción no podrá ser revertida",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d30000',
        confirmButtonText: 'Yes, eliminar',
        cancelButtonText: 'Cancelar',
    }).then(result => {
        if(result.isConfirmed) {
            fetch(url_fetch, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    cod_item: item_id
                })
            })
            .then(response => {
                return response.json();
            })
            .then(async d => {
                await showItems();
                Swal.fire({
                    position: 'center',
                    icon: d.status,
                    title: d.msg,
                    confirmButtonColor: '#19ec27',
                    confirmButtonText: 'ACEPTAR',
                })
            })
            .catch(e => {
                Swal.fire({
                    position: 'center',
                    icon: "error",
                    title: "Error al buscar actividad",
                    confirmButtonColor: '#df1c11',
                    confirmButtonText: 'ACEPTAR',
                })
            })
        }
    })
}

form.addEventListener("submit", (e) => {
    e.preventDefault();

    let isIdValid = checkInput(e.target.cod_item.value),
        isNameValid = checkInput(e.target.name_item.value);
    let isFormValid = isIdValid && isNameValid;
    if(isFormValid) {
        createItem(
            e.target.cod_item.value,
            e.target.name_item.value,
            e.target.quantity_item.value
        );
    } else {
        Swal.fire({
            position: 'center',
            icon: 'warning',
            title: 'Todos los campos son requeridos',
            confirmButtonColor: '#d33',
            confirmButtonText: 'Accept',
        })
    }
})

form_update.addEventListener("submit", (e) => {
    e.preventDefault();

    let isIdValid = checkInput(e.target.id_.value),
        isNameValid = checkInput(e.target.new_name.value),
        isStuckValid = checkInput(e.target.new_stuck.value);
    let isFormValid = isIdValid && isNameValid && isStuckValid;
    if(isFormValid) {
        modifyItem();
    } else {
        Swal.fire({
            position: 'center',
            icon: 'warning',
            title: 'Todos los campos son requeridos',
            confirmButtonColor: '#d33',
            confirmButtonText: 'Accept',
        })
    }
})