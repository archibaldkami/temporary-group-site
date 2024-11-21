import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, message TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS subcategories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category_id INTEGER, FOREIGN KEY (category_id) REFERENCES categories (id))')
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, image TEXT, category_id INTEGER, subcategory_id INTEGER, FOREIGN KEY (category_id) REFERENCES categories (id), FOREIGN KEY (subcategory_id) REFERENCES subcategories (id))')
    conn.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, address TEXT, total_price REAL, status TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS order_items (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, product_id INTEGER, quantity INTEGER, FOREIGN KEY (order_id) REFERENCES orders (id), FOREIGN KEY (product_id) REFERENCES products (id))')
    conn.commit()
    # category_id INTEGER, FOREIGN KEY (category_id) REFERENCES categories (id), 
    # subcategory_id INTEGER, FOREIGN KEY (subcategory_id) REFERENCES subcategories (id)
    conn.close()

def get_products_by_category(category_id):
    products = get_products()
    return [p for p in products if p['category'] == category_id]

def get_products_by_subcategory(subcategory_id):
    products = get_products()
    return [p for p in products if p['subcategory'] == subcategory_id]

def get_products_list() -> list[dict]: 
    """Get list with item dicts"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    products = [dict(p) for p in products]
    conn.close()
    return products

def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return products

def add_order(email, address, cart):
    conn = get_db_connection()
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    cur = conn.cursor()
    cur.execute('INSERT INTO orders (email, address, total_price, status, date) VALUES (?, ?, ?, ?, ?)',
                (email, address, total_price, 'New', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    order_id = cur.lastrowid
    for item in cart.values():
        cur.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)',
                    (order_id, item['id'], item['quantity']))
    conn.commit()
    conn.close()

def get_orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return orders

def get_all_categories_with_subcategories():
    """Отримує всі категорії з їх підкатегоріями"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Отримуємо всі категорії
    cursor.execute('SELECT id, name FROM categories')
    categories = [dict(cat) for cat in cursor.fetchall()]
    
    # Для кожної категорії отримуємо її підкатегорії
    for category in categories:
        cursor.execute('SELECT id, name FROM subcategories WHERE category_id = ?', (category['id'],))
        category['subcategories'] = [dict(sub) for sub in cursor.fetchall()]
    
    conn.close()
    return categories

def get_product_categories(product):
    """Отримує інформацію про категорію та підкатегорію продукту"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Отримуємо інформацію про категорію
    cursor.execute('SELECT name FROM categories WHERE id = ?', (product['category_id'],))
    category_result = cursor.fetchone()
    category_name = dict(category_result)['name'] if category_result else "Невідома категорія"
    
    # Отримуємо інформацію про підкатегорію
    cursor.execute('''
        SELECT s.name as subcategory_name, c.name as category_name 
        FROM subcategories s 
        JOIN categories c ON s.category_id = c.id 
        WHERE s.id = ?
    ''', (product['subcategory_id'],))
    subcategory_result = cursor.fetchone()
    
    conn.close()
    
    if subcategory_result:
        subcategory_result = dict(subcategory_result)
        # Перевіряємо, чи підкатегорія належить до правильної категорії
        if subcategory_result['category_name'] == category_name:
            subcategory_name = subcategory_result['subcategory_name']
        else:
            subcategory_name = "Невідповідна підкатегорія"
    else:
        subcategory_name = "Невідома підкатегорія"
    
    return category_name, subcategory_name

# def get_categories():
#     conn = get_db_connection()
#     categories = conn.execute('SELECT * FROM categories').fetchall()
#     categories = [dict(p) for p in categories]
#     conn.close()
#     return categories

# def get_subcategories():
#     conn = get_db_connection()
#     subcategories = conn.execute('SELECT * FROM subcategories').fetchall()
#     subcategories = [dict(p) for p in subcategories]
#     conn.close()
#     return subcategories

def get_category_name(category_id):
    """Отримує назву категорії за її id"""
    conn = get_db_connection() 
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM categories WHERE id = ?', (category_id,))
    result = cursor.fetchone()
    conn.close()
    return result['name'] if result else "Невідома категорія"

def get_subcategory_name(subcategory_id):
    """Отримує назву підкатегорії за її id"""
    conn = get_db_connection() 
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM subcategories WHERE id = ?', (subcategory_id,))
    result = cursor.fetchone()
    conn.close()
    return result['name'] if result else "Невідома категорія"

def get_order_details(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    items = conn.execute('SELECT oi.quantity, p.name, p.price FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE oi.order_id = ?', (order_id,)).fetchall()
    conn.close()
    return order, items

def update_order_status(order_id, status):
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()

def delete_order(order_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM order_items WHERE order_id = ?', (order_id,))
    conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()