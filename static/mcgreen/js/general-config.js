document.body.querySelectorAll("[hidden]").forEach((el, i) => {
    if(el.getAttribute("hidden") != null) {
        el.style.display = 'none';
    }
})