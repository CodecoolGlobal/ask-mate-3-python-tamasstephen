document.addEventListener('DOMContentLoaded', ()=> {

    const checkboxAll = document.querySelectorAll(".check_me");
    const menuButton = document.querySelector("#menu_more");
    const menuDropdown = document.querySelector(".dropdown");
    const dropdownAll = document.querySelectorAll(".dropdown");
    const showAnswers = document.querySelectorAll(".dropdown_link");
    const closeFlash = document.querySelector(".close");

    if (showAnswers) {
        showAnswers.forEach(link => {
            link.addEventListener('click', (e)=>{
                e.currentTarget.nextElementSibling.classList.toggle("collapse");
                e.currentTarget.textContent = e.currentTarget.textContent === "Show answers" ? "Hide answers" : "Show answers";
            })
        })
    }

    if (menuButton) {
        menuButton.addEventListener('click', (e)=>{
           menuButton.classList.toggle('open');
           menuDropdown.classList.toggle("collapsed");
        })
        }

   if (closeFlash) {
       closeFlash.addEventListener('click', removeWindow);
   }

    checkboxAll.forEach(checkbox => checkbox.addEventListener('click', fireSubmit))
    window.addEventListener('click', (e)=>{
        dropdownAll.forEach((dropdown )=> {
            const classes = Array.from(dropdown.classList);
            console.log(e.target)
            if(!classes.includes("collapsed") && e.target !== menuButton && e.target !== menuDropdown) {
                dropdown.classList.add("collapsed");
                menuButton.classList.remove("open");
            }
        })
    })


})

function fireSubmit(e) {
    const currentForm = e.currentTarget.closest("form");
    let submitEvent = new SubmitEvent("submit");
    currentForm.dispatchEvent(submitEvent)
}

function removeWindow(e) {
    let popupWindow = e.currentTarget.closest("div");
    popupWindow.remove()
}