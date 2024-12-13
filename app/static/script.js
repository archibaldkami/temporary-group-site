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



document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.dataset.productId;

            fetch(`/cart/remove/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    location.reload();
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

const categorySelect = document.getElementById('category');
const subcategorySelect = document.getElementById('subcategory');
const allSubcategories = Array.from(subcategorySelect.options);

categorySelect.addEventListener('change', function () {
    const selectedCategory = this.value;

    subcategorySelect.innerHTML = '<option value="">Оберіть підкатегорію</option>';

    const filteredSubcategories = allSubcategories.filter(option => 
        option.dataset.category === selectedCategory
    );

    filteredSubcategories.forEach(option => {
        const exists = Array.from(subcategorySelect.options).some(
            existingOption => existingOption.value === option.value
        );

        if (!exists) {
            subcategorySelect.appendChild(option);
        }
    });

    subcategorySelect.value = "";
    subcategorySelect.disabled = filteredSubcategories.length === 0;
});