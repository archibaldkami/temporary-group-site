from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from models import get_db_connection
from functools import wraps  # Add this import

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Ви маєте бути авторизовані')
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        
        cursor.execute('''
            UPDATE users 
            SET name = ?, phone = ?, address = ? 
            WHERE id = ?
        ''', (name, phone, address, session['user_id']))
        conn.commit()
        session['user_name'] = name
        
        flash('Профіль успішно оновлено')
        return redirect(url_for('auth.profile'))
    
    orders = []
    seller_products = []
    
    if user != None:
        if user['role'] == 'buyer':
            cursor.execute('SELECT * FROM orders WHERE email = ?', (user['email'],))
            orders = cursor.fetchall()
        
        elif user['role'] == 'seller':
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
        
        cursor.execute('''
            UPDATE users 
            SET name = ?, phone = ?, address = ? 
            WHERE id = ?
        ''', (name, phone, address, session['user_id']))
        
        conn.commit()
        conn.close()
        session['user_name'] = name
        
        flash('Профіль успішно оновлено')
        return redirect(url_for('auth.profile'))
    
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
        role = request.form['role']
        
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.islower() for char in password):
            flash('Пароль повинен бути не менше 8 символів та містити цифри і малі літери')
            return redirect(url_for('auth.register'))
        
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
                session['user_id'] = user['id']
                session['user_role'] = user['role']
                session['user_name'] = user['name']
                
                flash('Вхід успішний!')
                return redirect(url_for('auth.profile'))
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