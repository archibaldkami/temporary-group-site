from models import get_db_connection, init_db

def seed_products():
    init_db()  # Спочатку ініціалізуємо базу даних
    conn = get_db_connection()
    categories = [
        ('Взуття')
    ]
    
    conn.executemany('INSERT INTO categories (name) VALUES (?)', categories)
    # conn.execute('INSERT INTO categories (name) VALUES (?)', ('Взуття',))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_products()
    print("Категорії додано до бази даних.")