let headerBurgerBtn = document.querySelector(".header__burger")
let headerNav = document.querySelector(".header__nav")
let body = document.body

headerBurgerBtn.addEventListener("click", () => {
	headerBurgerBtn.classList.toggle("active")
	headerNav.classList.toggle("active")
	body.classList.toggle("fixed")
})