const navToggle = document.querySelector(".nav-toggle")
const navMenu = document.querySelector(".nav-menu")

navToggle.addEventListener("click",()=>{
    navMenu.classList.toggle("nav-menu_visible");
    
    if (navMenu.classList.contains("nav-menu_visible")) {
        navToggle.setAttribute("aria-label", "Cerrar menú");
      } else {
        navToggle.setAttribute("aria-label", "Abrir menú");
      }
});

const menuLinks = document.querySelectorAll('.nav-menu a[href^="#"');

menuLinks.forEach(menuLinks => {
  menuLinks.addEventListener("click",function(){
    navMenu.classList.toggle("nav-menu_visible")
  })
})