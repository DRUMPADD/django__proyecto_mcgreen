let sl_providers = document.querySelector(".sl_providers")
let form = document.querySelector(".form_create");
let btn = document.querySelector(".select_option");

let newProvBox = document.querySelector(".content-new-prov");
let prov_box = document.getElementById("provider-content");

let btn_mod_car = document.querySelector(".select-mod-car");
let btn_cancel = document.querySelector("#cancel-car");
let btn_del_car = document.querySelector("#delete-car");
let i_del_c = document.querySelector(".del-car");
let i_mod_c = document.querySelector(".mod-car");
let inputs_car = document.querySelectorAll(".inp_car");
let form_car = document.querySelector(".form-caracteristics");
let btn_sub_car = document.querySelector(".update-car");

btn_mod_car.addEventListener("click", () => {
    inputs_car.forEach(element => {
        element.removeAttribute("disabled");
        element.classList.add("border-active")
    })
    btn_del_car.style.display = "none";
    btn_cancel.style.display = "inline-block";
    btn_mod_car.style.display = "none";
    btn_sub_car.style.display = "inline-block";
})
btn_cancel.addEventListener("click", () => {
    inputs_car.forEach(element => {
        element.setAttribute("disabled", "");
        element.classList.remove("border-active")
    })
    btn_del_car.style.display = "inline-block";
    btn_cancel.style.display = "none";
    btn_mod_car.style.display = "inline-block";
    btn_sub_car.style.display = "none";
})

btn_del_car.addEventListener("click", () => {
    Swal.fire({
        title: "Las características serán eliminadas, ¿desea continuar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#df1c11',
        confirmButtonText: 'Si, eliminar',
        cancelButtonText: 'Cancelar',
    }).then(res => {
        if(res.isConfirmed) {
            updateCaracteristics({
                item_id: form_car["id"].value,
                name_: null,
                quantity: 0,
                brand: null,
                bought_date: null,
                state: null,
                model: null,
                serial_n: null,
                location: null,
                date_: null,
            });
        }
    })
})

form_car.addEventListener("submit", (e) => {
    e.preventDefault();
    for(let i = 0; i < form_car.elements.length; i++) {
        if(form_car.elements[i].type != "button" && form_car.elements[i].type != "submit") {
            console.log(form_car.elements[i].name+":", form_car.elements[i].value,"- tipo:", typeof form_car.elements[i].value);
        }
    }

    updateCaracteristics({
        item_id: form_car["id"].value,
        name_: form_car["name"].value,
        quantity: form_car["quantity"].value,
        brand: form_car["brand"].value,
        bought_date: form_car["bought_date"].value,
        state: form_car["sl_state"].value,
        model: form_car["model"].value,
        serial_n: form_car["serial_n"].value,
        location: form_car["location"].value,
        date_: form_car["date_"].value,
    });


})

if(prov_box.getElementsByClassName("id").length == 0) {
    btn.addEventListener("click", () => {
        if(sl_providers.value === "NUEVO") {
            newProvBox.style.display = "flex";
            newProvBox.style.visibility = "visible";
            newProvBox.style.opacity = 1;
        } else {
            newProvBox.style.display = "none";
            newProvBox.style.visibility = "hidden";
            newProvBox.style.opacity = 0;
        }
    })
    
    async function getProviders () {
        let response = await fetch("/plataforma/proveedor/mostrarProveedores");
        let data = await response.json();
        return data.msg;
    }
    
    async function showProviders () {
        let providers = await getProviders();
        let ar_prov = new Array(providers);
        let str_prov = "";
    
        str_prov += `<option selected disabled>--Seleccionar--</option>`
        
        ar_prov[0].forEach(element => {
            if(element.length !== 0) {
                str_prov += `
                <option value="${element[0]}">${element[1]}</option>
                `
            }
        });
        
        str_prov += `<option value="NUEVO">Nuevo proveedor</option>`
        
        sl_providers.innerHTML = str_prov;
    }

    window.addEventListener("DOMContentLoaded", () => {
        showProviders();
    })

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        let ar_answers = new Array();
        if(form.elements[2].value != "--Seleccionar--" && form.elements[2].value == "NUEVO") {
            for(let i = 0; i < form.elements.length - 1; i++) {
                if(form.elements[i].type != "button" && form.elements[i].type != "submit") {
                    ar_answers.push(form.elements[i].value)
                }
            }
        } else {
            for(let i = 0; i < form.elements.length - 6; i++) {
                if(form.elements[i].type != "button" && form.elements[i].type != "submit") {
                    ar_answers.push(form.elements[i].value)
                }
            }
        }
        if(ar_answers.length > 3) {
            ar_answers.splice(2, 1)
            register_add_provider({
                item_id: ar_answers[1],
                prov_id: ar_answers[2],
                p_nombre: ar_answers[3],
                numero_t: ar_answers[4],
                email: ar_answers[5],
                country: ar_answers[6],
            })
        } else {
            register_add_provider({
                item_id: ar_answers[1],
                prov_id: ar_answers[2]
            })
        }
    })
} else {
    
    let btn_mod = document.querySelector(".select-mod");
    let btn_del_prov = document.querySelector("#delete");
    let btn_cancel = document.querySelector("#cancel");
    
    let inputs_ = document.querySelectorAll(".input_prov");
    let form_prov = document.querySelector(".form-provider");
    let btn_sub_mod = document.querySelector(".update-mod");

    btn_del_prov.addEventListener("click", () => {
        const getData = btn_del_prov.parentElement;
        delete_prov_from_item({
            id: getData.getAttribute("id-item"),
        })
    })

    btn_mod.addEventListener("click", () => {
        inputs_.forEach(element => {
            element.removeAttribute("disabled");
            element.classList.add("border-active")
        })
        btn_mod.style.display = "none";
        btn_sub_mod.style.display = "inline-block";
        btn_cancel.style.display = "inline-block";
        btn_del_prov.style.display = "none";
    })
    
    btn_cancel.addEventListener("click", () => {
        inputs_.forEach(element => {
            element.setAttribute("disabled", "");
            element.classList.remove("border-active")
        })
        btn_cancel.style.display = "none";
        btn_del_prov.style.display = "inline-block";
        btn_sub_mod.style.display = "none";
        btn_mod.style.display = "inline-block";
    })

    form_prov.addEventListener("submit", (e) => {
        e.preventDefault();
        modifyProvider({
            nombre: form_prov["prov_nam"].value,
            telefono: form_prov["phone"].value,
            email: form_prov["email"].value,
            pais: form_prov["country"].value,
            cod_prov: form_prov["id_prov"].value,
        })
    })

    let box_update_form = document.getElementById("prov-content");
    let form_update = document.querySelector(".form_update");
    let btn_change = document.querySelector(".btn-change");
    let btnClose = document.querySelector(".btnClose");

    btnClose.addEventListener("click", () => {
        box_update_form.style.visibility = "hidden";
        box_update_form.style.opacity = 0;
    });

    btn_change.addEventListener("click", (e) => {
        box_update_form.style.visibility = "visible";
        box_update_form.style.opacity = 1;
        const parentTR = btn_change.parentElement.parentElement;
        form_update["sl_providers"].value = parentTR.querySelector("#id_prov").value;
    });

    form_update.addEventListener("submit", (e) => {
        e.preventDefault();
        changeProvider({
            item_id: form_update["id_item"].value,
            prov_id: form_update["sl_providers"].value,
        });
    })
}

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

function register_add_provider(values) {
    fetch("/plataforma/proveedor/agregarProveedorAItem", {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(values)
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
        location.reload();
    })
    .catch(e => {
        console.log(e);
        Swal.fire({
            position: 'center',
            icon: "error",
            title: "Error al agregar nuevo proveedor a item",
            confirmButtonColor: '#df1c11',
            confirmButtonText: 'ACEPTAR',
        })
    })
}

function modifyProvider(values) {
    fetch("/plataforma/proveedor/modificarProveedor", {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(values)
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
        location.reload();
    })
    .catch(e => {
        console.log(e);
        Swal.fire({
            position: 'center',
            icon: "error",
            title: "Error al modificar proveedor",
            confirmButtonColor: '#df1c11',
            confirmButtonText: 'ACEPTAR',
        })
    })
}

function updateCaracteristics(values) {
    fetch("/plataforma/equipo/modificarCaracteristicas", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(values)
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
        location.reload();
    })
    .catch(e => {
        console.log(e);
        Swal.fire({
            position: 'center',
            icon: "error",
            title: "Error al modificar características",
            confirmButtonColor: '#df1c11',
            confirmButtonText: 'ACEPTAR',
        })
    })
}

function changeProvider(values) {
    fetch("/plataforma/proveedor/cambiarProveedor", {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(values)
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
        location.reload();
    })
    .catch(e => {
        console.log(e);
        Swal.fire({
            position: 'center',
            icon: "error",
            title: "Error al cambiar proveedor",
            confirmButtonColor: '#df1c11',
            confirmButtonText: 'ACEPTAR',
        })
    })
}

function delete_prov_from_item(values) {
    Swal.fire({
        title: "El proveedor será removido de este item, ¿desea continuar?",
        text: "Esta acción no podrá ser revertida",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#df1c11',
        confirmButtonText: 'Si, eliminar',
        cancelButtonText: 'Cancelar',
    }).then(result => {
        if(result.isConfirmed) {
            fetch("/plataforma/proveedor/quitarProveedor", {
                method: 'POST',
                headers: {
                    "Accept": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(values)
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
                location.reload();
            })
            .catch(e => {
                console.log(e);
                Swal.fire({
                    position: 'center',
                    icon: "error",
                    title: "Error al cambiar proveedor",
                    confirmButtonColor: '#df1c11',
                    confirmButtonText: 'ACEPTAR',
                })
            })
        }
    })
}