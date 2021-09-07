document.addEventListener('DOMContentLoaded', ()=> {

    const checkboxAll = document.querySelectorAll(".check_me");
    checkboxAll.forEach(checkbox => checkbox.addEventListener('click', fireSubmit))
})

function fireSubmit(e) {
    const currentForm = e.currentTarget.closest("form");
    let submitEvent = new SubmitEvent("submit");
    currentForm.dispatchEvent(submitEvent)
}

