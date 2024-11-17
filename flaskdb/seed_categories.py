from models import get_db_connection, init_db

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

if __name__ == '__main__':
    seed_categories()
    print("Категорії додано до бази даних.")




# sub_categories = [
#     ('Футболки', 1),    
#     ('Сорочки', 1),   
#     ('Сукні', 2),      
#     ('Спідниці', 2),  
#     ('Куртки', 3),      
#     ('Кросівки', 4),  
#     ('Сумки', 5),    
#     ('Ремені', 5)     
# ]