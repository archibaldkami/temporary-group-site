# Документація REST API для магазину

## Базова URL адреса API
```
http://127.0.0.1:5003/api
```

## Endpoints

### Товари (Products)

#### Отримати всі товари
Отримує список всіх доступних товарів.

**Запит:**
```http
GET /api/products
```

**Відповідь:**
```json
[
    {
        "category_id": 1,
        "id": 1,
        "image": "images/mens_tshirt.jpg",
        "name": "Чоловіча футболка",
        "price": 500.0,
        "seller_id": null,
        "subcategory_id": 1
    },
    {
        "category_id": 1,
        "id": 2,
        "image": "images/mens_shirt.jpg",
        "name": "Чоловіча сорочка",
        "price": 700.0,
        "seller_id": null,
        "subcategory_id": 2
    },
    {
        "category_id": 2,
        "id": 3,
        "image": "images/womens_dress.jpg",
        "name": "Жіноча сукня",
        "price": 1200.0,
        "seller_id": null,
        "subcategory_id": 3
    },
    {
        "category_id": 2,
        "id": 4,
        "image": "images/womens_skirt.jpg",
        "name": "Жіноча спідниця",
        "price": 900.0,
        "seller_id": null,
        "subcategory_id": 4
    },
    {
        "category_id": 3,
        "id": 5,
        "image": "images/kids_jacket.jpg",
        "name": "Дитяча куртка",
        "price": 1500.0,
        "seller_id": null,
        "subcategory_id": 5
    },
    {
        "category_id": 4,
        "id": 6,
        "image": "images/nike_sneakers.jpg",
        "name": "Кросівки Nike",
        "price": 2500.0,
        "seller_id": null,
        "subcategory_id": 6
    },
    {
        "category_id": 5,
        "id": 7,
        "image": "images/leather_bag.jpg",
        "name": "Шкіряна сумка",
        "price": 2000.0,
        "seller_id": null,
        "subcategory_id": 7
    },
    {
        "category_id": 5,
        "id": 8,
        "image": "images/mens_belt.jpg",
        "name": "Чоловічий ремінь",
        "price": 800.0,
        "seller_id": null,
        "subcategory_id": 8
    },
    {
        "category_id": 5,
        "id": 9,
        "image": "images/photo_2023-03-26_21-25-25.jpg",
        "name": "Кітик з ножом",
        "price": 999.99,
        "seller_id": 2,
        "subcategory_id": 8
    }
]
```

**Коди статусу:**
- 200: Успішно
- 500: error

---

### Замовлення (Orders)

#### Отримати деталі замовлення.

**Запит:**
```http
GET /api/orders
```

**Відповідь:**
```json
[
    {
        "address": "Київ",
        "date": "2024-12-13 02:20:28",
        "email": "romanykandr0101@gmail.com",
        "id": 1,
        "status": "New",
        "total_price": 3000.0
    }
]

---

### Відгуки (Feedback)

#### Переглянути відгуки

**Запит:**
```http
POST /api/feedback
```

**Відповідь:**
[
    {
        "date": "2024-11-30 19:14:09",
        "email": "archibaldkami@proton.me",
        "id": 1,
        "message": "Мурчить забагато",
        "name": "archibaldkami@proton.me",
        "product_id": 9
    },
    {
        "date": "2024-11-30 19:14:55",
        "email": "admin@admin",
        "id": 2,
        "message": "Ніж прикольний",
        "name": "admin",
        "product_id": 9
    },
    {
        "date": "2024-11-30 19:17:57",
        "email": "archibaldkami@proton.me",
        "id": 3,
        "message": "Червоненький",
        "name": "Мяу",
        "product_id": 9
    },
    {
        "date": null,
        "email": "admin@admin",
        "id": 4,
        "message": "Привіт",
        "name": "admin",
        "product_id": null
    }
]

#### Переглянути конкретний відгук

**Запит:**
```http
POST /api/feedback?id=1
```

**Відповідь:**
[
    {
        "date": "2024-11-30 19:14:09",
        "email": "archibaldkami@proton.me",
        "id": 1,
        "message": "Мурчить забагато",
        "name": "archibaldkami@proton.me",
        "product_id": 9
    }
