/* Filename: script.js*/

const burger = document.querySelector('#burger');
const navMenu = document.querySelector('#nav-menu');

burger.addEventListener('click', () => {
    burger.classList.toggle('active');
    navMenu.style.height = navMenu.style.height === '64px' ? '0' : '64px';
});


document.addEventListener('DOMContentLoaded', () => {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-ajax');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const url = button.getAttribute('data-url');

            fetch(url, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    // alert("Товар додано до кошика!");
                    // Оновіть інтерфейс кошика, якщо потрібно
                } else {
                    alert("Помилка: " + data.message);
                }
            })
            .catch(error => {
                console.error('Помилка:', error);
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const addToWishlistButtons = document.querySelectorAll('.add-to-wishlist-ajax');

    addToWishlistButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const url = button.getAttribute('data-url');

            fetch(url, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    // alert("Товар додано до бажаного!");
                    // Оновіть інтерфейс кошика, якщо потрібно
                } else {
                    alert("Помилка: " + data.message);
                }
            })
            .catch(error => {
                console.error('Помилка:', error);
            });
        });
    });
});





// Отримуємо елементи категорії та підкатегорії
const categorySelect = document.getElementById('category');
const subcategorySelect = document.getElementById('subcategory');
const allSubcategories = Array.from(subcategorySelect.options);

// Обробник зміни категорії
categorySelect.addEventListener('change', function () {
    const selectedCategory = this.value;

    // Очищаємо список підкатегорій, залишаючи лише "Оберіть підкатегорію"
    subcategorySelect.innerHTML = '<option value="">Оберіть підкатегорію</option>';

    // Фільтруємо підкатегорії за обраною категорією
    const filteredSubcategories = allSubcategories.filter(option => 
        option.dataset.category === selectedCategory
    );

    // Додаємо відфільтровані підкатегорії без повторів
    filteredSubcategories.forEach(option => {
        const exists = Array.from(subcategorySelect.options).some(
            existingOption => existingOption.value === option.value
        );

        if (!exists) {
            subcategorySelect.appendChild(option);
        }
    });

    // Встановлюємо початкове значення "Оберіть підкатегорію"
    subcategorySelect.value = "";

    // Деактивуємо підкатегорії, якщо немає доступних варіантів
    subcategorySelect.disabled = filteredSubcategories.length === 0;
});