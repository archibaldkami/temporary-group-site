from models import get_db_connection, init_db

def seed_products():
    init_db()  # Спочатку ініціалізуємо базу даних
    conn = get_db_connection()
    products = [
        ('Чоловіча футболка', 500, 'images/mens_tshirt.jpg', 1, 1),
        ('Чоловіча сорочка', 700, 'images/mens_shirt.jpg', 1, 2),
        ('Жіноча сукня', 1200, 'images/womens_dress.jpg', 2, 3),
        ('Жіноча спідниця', 900, 'images/womens_skirt.jpg', 2, 4),
        ('Дитяча куртка', 1500, 'images/kids_jacket.jpg', 3, 5),
        ('Кросівки Nike', 2500, 'images/nike_sneakers.jpg', 4, 6),
        ('Шкіряна сумка', 2000, 'images/leather_bag.jpg', 5, 7),
        ('Чоловічий ремінь', 800, 'images/mens_belt.jpg', 5, 8)
    ]
    
    conn.executemany('INSERT INTO products (name, price, image, category_id, subcategory_id) VALUES (?, ?, ?, ?, ?)', products)
    conn.commit()
    conn.close()
    print("Тестові продукти додано до бази даних.")

def seed_subcategories():
    init_db()  # Спочатку ініціалізуємо базу даних
    conn = get_db_connection()
    subcategories = [
        ('Футболки', 1),    
        ('Сорочки', 1),   
        ('Сукні', 2),      
        ('Спідниці', 2),  
        ('Куртки', 3),      
        ('Кросівки', 4),  
        ('Сумки', 5),    
        ('Ремені', 5)     
    ]
    # id = (1)
    conn.executemany('INSERT INTO subcategories (name, category_id) VALUES (?, ?)', subcategories)
    # conn.execute('DELETE FROM subcategories WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    print("Тестові підкатегорії додано до бази даних.")
    

def seed_categories():
    init_db()  # Спочатку ініціалізуємо базу даних
    conn = get_db_connection()
    categories = [
        ('Чоловічий одяг', ),
        ('Жіночий одяг', ),
        ('Дитячий одяг', ),
        ('Взуття', ),
        ('Аксесуари', )
    ]
    
    # conn.executemany('INSERT INTO categories (name) VALUES (?)', categories)
    for i in categories:

        conn.execute('INSERT INTO categories (name) VALUES (?)', i)
    conn.commit()
    conn.close()
    print("Тестові категорії додано до бази даних.")

if __name__ == '__main__':
    seed_categories()
    seed_subcategories()
    seed_products()
    print("Тестові категорії додано до бази даних.")
    print("Тестові підкатегорії додано до бази даних.")
    print("Тестові продукти додано до бази даних.")