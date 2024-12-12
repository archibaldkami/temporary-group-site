from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import get_db_connection, get_orders, get_order_details, update_order_status, delete_order
from routes.auth import role_required
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@role_required(['admin'])
def admin():
    conn = get_db_connection()
    
    # Отримання даних для адмін-панелі
    feedback = conn.execute('SELECT * FROM feedback').fetchall()
    users = conn.execute('SELECT * FROM users').fetchall()
    products = conn.execute('SELECT * FROM products').fetchall()
    
    conn.close()
    
    orders = get_orders()
    return render_template('admin.html', 
                           feedback=feedback, 
                           orders=orders, 
                           users=users, 
                           products=products)

# Функції для керування користувачами
@admin_bp.route('/admin/add_user', methods=['GET', 'POST'])
@role_required(['admin'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']
        role = request.form['role']
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # Перевірка чи існує вже користувач з таким email
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                flash('Користувач з таким email вже існує')
            else:

                conn.execute('''
                    INSERT INTO users (name, email, phone, address, password, role) 
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, email, phone, address, hashed_password, role))
                conn.commit()
                flash('Користувач успішно доданий!')
        except Exception as e:
            flash(f'Помилка додавання користувача: {str(e)}')
        finally:
            conn.close()
        
        return redirect(url_for('admin.admin'))
    
    return render_template('add_user.html')

@admin_bp.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@role_required(['admin'])
def edit_user(user_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        role = request.form['role']
        
        conn.execute('''
            UPDATE users 
            SET name = ?, email = ?, phone = ?, address = ?, role = ?
            WHERE id = ?
        ''', (name, email, phone, address, role, user_id))
        conn.commit()
        flash('Дані користувача оновлено!')
        return redirect(url_for('admin.admin'))
    
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    return render_template('edit_user.html', user=dict(user))

@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@role_required(['admin'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    flash('Користувача видалено!')
    return redirect(url_for('admin.admin'))

# Функції для керування товарами
@admin_bp.route('/admin/add_product', methods=['GET', 'POST'])
@role_required(['admin'])
def add_product():
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category_id = request.form['category_id']
        
        conn.execute('''
            INSERT INTO products (name, price, category_id) 
            VALUES (?, ?, ?)
        ''', (name, price, category_id))
        conn.commit()
        flash('Товар успішно додано!')
        return redirect(url_for('admin.admin'))
    
    categories = conn.execute('SELECT * FROM categories').fetchall()
    subcategories = conn.execute('SELECT * FROM subcategories').fetchall()
    conn.close()
    
    return render_template('admin_add_product.html', categories=categories, subcategories=subcategories)

@admin_bp.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
@role_required(['admin'])
def edit_product(product_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category_id = request.form['category_id']
        subcategory_id = request.form['subcategory_id']
        
        conn.execute('''
            UPDATE products 
            SET name = ?, price = ?, category_id = ?, subcategory_id = ?
            WHERE id = ?
        ''', (name, price, category_id, subcategory_id, product_id))
        conn.commit()
        flash('Товар оновлено!')
        return redirect(url_for('admin.admin'))
    
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    subcategories = conn.execute('SELECT * FROM subcategories').fetchall()
    conn.close()
    
    return render_template('admin_edit_product.html', product=dict(product), categories=categories, subcategories=subcategories)

@admin_bp.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@role_required(['admin'])
def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    
    flash('Товар видалено!')
    return redirect(url_for('admin.admin'))

# Попередні функції залишаються без змін
@admin_bp.route('/admin/delete_feedback/<int:id>', methods=['POST'])
@role_required(['admin'])
def delete_feedback(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM feedback WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/order/<int:order_id>')
@role_required(['admin'])
def order_details(order_id):
    order, items = get_order_details(order_id)
    return render_template('admin_order_details.html', order=order, items=items)

@admin_bp.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
@role_required(['admin'])
def update_order(order_id):
    status = request.form['status']
    update_order_status(order_id, status)
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/delete_order/<int:order_id>', methods=['POST'])
@role_required(['admin'])
def delete_order_route(order_id):
    delete_order(order_id)
    return redirect(url_for('admin.admin'))