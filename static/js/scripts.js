document.addEventListener('DOMContentLoaded', ()=> {

    const checkboxAll = document.querySelectorAll(".check_me");
    const menuButton = document.querySelector("#menu_more");
    const menuDropdown = document.querySelector(".dropdown");

    menuButton.addEventListener('click', (e)=>{
       menuButton.classList.toggle('open');
       menuDropdown.classList.toggle("collapsed");
    })
    checkboxAll.forEach(checkbox => checkbox.addEventListener('click', fireSubmit))
})

function fireSubmit(e) {
    const currentForm = e.currentTarget.closest("form");
    let submitEvent = new SubmitEvent("submit");
    currentForm.dispatchEvent(submitEvent)
}

