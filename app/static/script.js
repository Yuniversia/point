function sendForm(formId, method) {
    form = document.getElementById(formId)

    fetch(form.action, {
        method: method,
        body: new FormData(form),
    })
    .then(response => response.json())
    .then(data => {
        const result = document.getElementById("main");
        const msg = data.message;
        const success = data.success;
        const reloadPage = data.reload;

        var icon = "fa-check-circle";
        var category = "success";

        if (success === false) {
            var icon = "fa-exclamation-circle";
            var category = "error";
        }

        if (reloadPage === true) {
            location.reload()
        }

        const div = `<div class='alert alert-${category} admin-alert'><i class='fas ${icon}'></i>
            ${msg}
            </div>`;
        
        result.innerHTML = ''
        result.innerHTML = div
    });
}