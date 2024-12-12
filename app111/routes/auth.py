from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from models import get_db_connection
from functools import wraps  # Add this import

auth_bp = Blueprint('auth', __name__)

# def get_db_connection():
#     conn = sqlite3.connect('db.sqlite')
#     conn.row_factory = sqlite3.Row
#     return conn

@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Ви маєте бути авторизовані')
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Отримання інформації про користувача
    cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    
    if request.method == 'POST':
        # Логіка оновлення профілю
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        
        cursor.execute('''
            UPDATE users 
            SET name = ?, phone = ?, address = ? 
            WHERE id = ?
        ''', (name, phone, address, session['user_id']))
        conn.commit()
        
        # Оновлення інформації в сесії
        session['user_name'] = name
        
        flash('Профіль успішно оновлено')
        return redirect(url_for('auth.profile'))
    
    # Додаткова інформація для різних ролей
    orders = []
    seller_products = []
    
    if user != None:
        if user['role'] == 'buyer':
            # Отримання замовлень покупця
            cursor.execute('SELECT * FROM orders WHERE email = ?', (user['email'],))
            orders = cursor.fetchall()
        
        elif user['role'] == 'seller':
            # Отримання товарів продавця
            cursor.execute('SELECT * FROM products WHERE seller_id = ?', (user['id'],))
            seller_products = cursor.fetchall()
    else: 
        return redirect(url_for('auth.login'))

    conn.close()
    
    
    return render_template('profile.html', 
                           user=dict(user), 
                           orders=orders, 
                           seller_products=seller_products)

@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Спочатку увійдіть в систему')
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        
        # Оновлення профілю
        cursor.execute('''
            UPDATE users 
            SET name = ?, phone = ?, address = ? 
            WHERE id = ?
        ''', (name, phone, address, session['user_id']))
        
        conn.commit()
        conn.close()
        
        # Оновлюємо дані в сесії
        session['user_name'] = name
        
        flash('Профіль успішно оновлено')
        return redirect(url_for('auth.profile'))
    
    # Отримання поточних даних користувача
    cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    
    return render_template('profile_edit.html', user=dict(user))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        if phone == None: phone = ''
        address = request.form['address']
        if address == None: address = ''
        password = request.form['password']
        role = request.form['role']  # Додаємо вибір ролі
        
        # Перевірка складності паролю
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.islower() for char in password):
            flash('Пароль повинен бути не менше 8 символів та містити цифри і малі літери')
            return redirect(url_for('auth.register'))
        
        # Хешування паролю
        hashed_password = generate_password_hash(password)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Перевірка чи існує вже користувач з таким email
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                flash('Користувач з таким email вже існує')
                return redirect(url_for('auth.register'))
            
            # Додавання нового користувача
            cursor.execute('''
                INSERT INTO users (name, email, phone, address, password, role) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, address, hashed_password, role))
            
            conn.commit()
            flash('Реєстрація успішна!')
            return redirect(url_for('auth.login'))
        
        except sqlite3.Error as e:
            flash(f'Помилка реєстрації: {e}')
        
        finally:
            conn.close()
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Пошук користувача за email
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], password):
                # Успішний вхід - зберігаємо інформацію про сесію
                session['user_id'] = user['id']
                session['user_role'] = user['role']
                session['user_name'] = user['name']
                
                flash('Вхід успішний!')
                return redirect(url_for('home'))
            else:
                flash('Невірний email або пароль')
        
        except sqlite3.Error as e:
            flash(f'Помилка входу: {e}')
        
        finally:
            conn.close()
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Декоратор для перевірки прав доступу
def role_required(roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] not in roles:
                flash('У вас немає прав для перегляду цієї сторінки')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return wrapper
    return decorator

# def role_required(roles):
#     def decorator(f):
#         @wraps(f)  # This is crucial to preserve the original function's metadata
#         def wrapper(*args, **kwargs):
#             if 'user_id' not in session:
#                 flash('Будь ласка, увійдіть в систему.')
#                 return redirect(url_for('auth.login'))
            
#             # Assuming you have a way to check the user's role
#             # This might involve a database query to get the user's role
#             user_role = get_user_role(session['user_id'])  # You'd need to implement this function
            
#             if user_role not in roles:
#                 flash('У вас немає дозволу на доступ до цієї сторінки.')
#                 return redirect(url_for('home'))
            
#             return f(*args, **kwargs)
#         return wrapper
#     return decorator
