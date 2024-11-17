from models import get_db_connection, init_db

def seed_products():
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

if __name__ == '__main__':
    seed_products()
    print("Підкатегорії додано до бази даних.")