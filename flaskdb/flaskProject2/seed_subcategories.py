from models import get_db_connection, init_db

def seed_products():
    init_db()  # Спочатку ініціалізуємо базу даних
    conn = get_db_connection()
    categories = [
        ('Кросівки', 1)
    ]
    id = (1)
    conn.executemany('INSERT INTO subcategories (name, category_id) VALUES (?, ?)', categories)
    # conn.execute('DELETE FROM subcategories WHERE id = ?', (id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_products()
    print("Підкатегорії додано до бази даних.")