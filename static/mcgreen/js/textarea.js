let textarea = document.querySelector(".textarea");
let current_value = document.getElementById("actual");
let total_value = document.getElementById("completo");

textarea.addEventListener("keyup", (e) => {
    let current = e.target.value.length;
    
    if(current <= 100) {
        current_value.style.color = "#000";
        total_value.style.color = "#000";
    } else if(current > 100 && current < 200) {
        current_value.style.color = "#a9ac03";
        total_value.style.color = "#a9ac03";
    } else if (current > 270) {
        current_value.style.color = "#da0101";
        total_value.style.color = "#da0101";
    }

    if (current < 301) {
        current_value.innerText = current;
    }
})