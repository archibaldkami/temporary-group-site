from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import get_db_connection
from routes.auth import role_required
import os

seller_bp = Blueprint('seller', __name__)

@seller_bp.route('/seller/dashboard')
@role_required(['seller'])
def dashboard():
    conn = get_db_connection()
    
    # Отримуємо лише товари поточного продавця
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE seller_id = ?', (session['user_id'],))
    products = [dict(product) for product in cursor.fetchall()]
    
    # Отримуємо замовлення для товарів продавця
    cursor.execute('''
        SELECT DISTINCT o.* 
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE p.seller_id = ?
    ''', (session['user_id'],))
    orders = [dict(order) for order in cursor.fetchall()]
    
    conn.close()
    
    return render_template('seller_dashboard.html', products=products, orders=orders)

@seller_bp.route('/seller/add_product', methods=['GET', 'POST'])
@role_required(['seller'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])
        subcategory_id = int(request.form.get('subcategory_id', 0))
        
        # Обробка зображення
        image = request.files.get('image')
        if image:
            filename = image.filename
            image.save(os.path.join('static/images', filename))
            image_path = f'images/{filename}'
        else:
            image_path = 'images/placeholder.jpg'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products 
            (name, price, image, category_id, subcategory_id, seller_id) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, price, image_path, category_id, subcategory_id, session['user_id']))
        
        conn.commit()
        conn.close()
        
        flash('Товар успішно додано!')
        return redirect(url_for('seller.dashboard'))
    
    # Отримання категорій для форми
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    subcategories = conn.execute('SELECT * FROM subcategories').fetchall()
    conn.close()
    
    return render_template('add_product.html', categories=categories, subcategories=subcategories)

@seller_bp.route('/seller/edit_product/<int:product_id>', methods=['GET', 'POST'])
@role_required(['seller'])
def edit_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Перевірка, чи належить товар поточному продавцю
    cursor.execute('SELECT * FROM products WHERE id = ? AND seller_id = ?', (product_id, session['user_id']))
    product = cursor.fetchone()
    
    if not product:
        flash('Ви не маєте прав редагувати цей товар')
        return redirect(url_for('seller.dashboard'))
    
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])
        subcategory_id = int(request.form['subcategory_id'])
        
        # Обробка зображення
        image = request.files.get('image')
        if image:
            filename = image.filename
            image.save(os.path.join('app/static/images', filename))
            image_path = f'images/{filename}'
        else:
            image_path = product['image']
        
        cursor.execute('''
            UPDATE products 
            SET name = ?, price = ?, image = ?, category_id = ?, subcategory_id = ?
            WHERE id = ?
        ''', (name, price, image_path, int(category_id), int(subcategory_id), product_id))
        
        conn.commit()
        conn.close()
        
        flash('Товар успішно оновлено!')
        return redirect(url_for('seller.dashboard'))
    
    # Отримання категорій для форми
    categories = conn.execute('SELECT * FROM categories').fetchall()

        # Отримання категорій для форми
    subcategories = conn.execute('SELECT * FROM subcategories').fetchall()
    
    conn.close()

    return render_template('edit_product.html', product=dict(product), categories=categories, subcategories=subcategories)

@seller_bp.route('/seller/delete_product/<int:product_id>', methods=['POST'])
@role_required(['seller'])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Перевірка, чи належить товар поточному продавцю
    cursor.execute('DELETE FROM products WHERE id = ? AND seller_id = ?', (product_id, session['user_id']))
    
    conn.commit()
    conn.close()
    
    flash('Товар успішно видалено!')
    return redirect(url_for('seller.dashboard'))

def validate_product_data(name, price):
    errors = []
    
    # Перевірка назви
    if len(name) < 3:
        errors.append("Назва товару має бути не менше 3 символів")
    if len(name) > 100:
        errors.append("Назва товару не може бути більше 100 символів")
    
    # Перевірка ціни
    try:
        price = float(price)
        if price < 0:
            errors.append("Ціна не може бути від'ємною")
    except ValueError:
        errors.append("Некоректна ціна")
    
    return errors