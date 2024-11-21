# archibald

from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
import os
from models import get_products_list, add_order, get_products,\
      get_products_by_category, get_products_by_subcategory, get_all_categories_with_subcategories, get_product_categories, \
      get_category_name, get_subcategory_name

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/category/<int:category_id>')
def category(category_id):
    products = get_products_by_category(category_id)
    return render_template('shop.html', products=products)

@shop_bp.route('/subcategory/<int:subcategory_id>')
def subcategory(subcategory_id):
    products = get_products_by_subcategory(subcategory_id)
    return render_template('shop.html', products=products)

@shop_bp.route('/shop')
def shop():
    category_id = request.args.get('category', type=int)
    subcategory_id = request.args.get('subcategory', type=int)
    search_query = request.args.get('search', '').strip()
    
    products = get_products_list()
    categories = get_all_categories_with_subcategories()
    
    # Фільтрація за пошуковим запитом
    if search_query:
        products = [p for p in products if 
                   search_query.lower() in p['name'].lower() or 
                   search_query.lower() in p.get('description', '').lower()]
    
    # Фільтр по категоріям та додавання їх імен до продукту
    if subcategory_id:
        products = [p for p in products if p['subcategory_id'] == subcategory_id]
    elif category_id:
        products = [p for p in products if p['category_id'] == category_id]

    for product in products:
        category_name, subcategory_name = get_product_categories(product)
        product['category_name'] = category_name
        product['subcategory_name'] = subcategory_name
        
        # +Зображення
        image_path = os.path.join(current_app.static_folder, 'images', os.path.basename(product['image']))
        if os.path.exists(image_path):
            product['image_url'] = url_for('static', filename=f"images/{os.path.basename(product['image'])}")
        else:
            product['image_url'] = url_for('static', filename='images/placeholder.jpg')
    
    return render_template('shop.html', products=products, categories=categories, selected_category=category_id, selected_subcategory=subcategory_id, search_query=search_query)


# Не те щоб тут багато змінювалось
@shop_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    products = get_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart = session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {'id': product_id, 'name': product['name'], 'price': product['price'], 'quantity': 1}
        session['cart'] = cart
    return redirect(url_for('shop.shop'))

@shop_bp.route('/cart/add_ajax/<int:product_id>', methods=['POST'])
def add_to_cart_ajax(product_id):
    products = get_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart = session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {'id': product_id, 'name': product['name'], 'price': product['price'], 'quantity': 1}
        session['cart'] = cart
        return {"status": "success", "message": "Product added to cart"}
    return {"status": "error", "message": "Product not found"}, 404


@shop_bp.route('/cart')
def cart():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@shop_bp.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        session['cart'] = cart
        return {"status": "success", "message": "Product removed from cart"}
    return {"status": "error", "message": "Product not found in cart"}, 404


@shop_bp.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    email = request.form['email']
    address = request.form['address']
    add_order(email, address, cart)
    session['cart'] = {}
    return redirect(url_for('shop.shop'))

@shop_bp.route('/favorite/add/<int:product_id>')
def add_to_favorite(product_id):
    products = get_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        favorite = session.get('favorite', {})
        if str(product_id) not in favorite:
            favorite[str(product_id)] = {
                'id': product_id,
                'name': product['name'],
                'price': product['price'],
                'image': product['image']
            }
        session['favorite'] = favorite
    return redirect(url_for('shop.shop'))

@shop_bp.route('/favorite/remove/<int:product_id>')
def remove_from_favorite(product_id):
    favorite = session.get('favorite', {})
    favorite.pop(str(product_id), None)
    session['favorite'] = favorite
    return redirect(url_for('shop.favorite'))

@shop_bp.route('/favorite')
def favorite():
    favorite = session.get('favorite', {})
    products = []
    for product_id, details in favorite.items():
        product = details.copy()
        # Додаємо URL зображення
        image_path = os.path.join(current_app.static_folder, 'images', os.path.basename(product['image']))
        if os.path.exists(image_path):
            product['image_url'] = url_for('static', filename=f"images/{os.path.basename(product['image'])}")
        else:
            product['image_url'] = url_for('static', filename='images/placeholder.jpg')
        products.append(product)
    return render_template('favorite.html', products=products)