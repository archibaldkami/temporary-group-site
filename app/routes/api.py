from flask import Blueprint, jsonify, request
from models import (
    get_db_connection,
    get_products,
    get_orders,
    get_users,
    get_order_details,
    add_order,
    update_order_status,
    delete_order
)

api_bp = Blueprint('api', __name__)

# Products endpoints
@api_bp.route('/api/products', methods=['GET'])
def get_all_products():
    try:
        products = get_products()
        return jsonify([dict(product) for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# # Users endpoints
@api_bp.route('/api/users', methods=['GET'])
def get_all_users():
    try:
        orders = get_users()
        return jsonify([dict(order) for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Orders endpoints
@api_bp.route('/api/orders', methods=['GET'])
def get_all_orders():
    try:
        orders = get_orders()
        return jsonify([dict(order) for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        order, items = get_order_details(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({
            'order': dict(order),
            'items': [dict(item) for item in items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'address' not in data or 'cart' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        add_order(data['email'], data['address'], data['cart'])
        return jsonify({'message': 'Order created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        update_order_status(order_id, data['status'])
        return jsonify({'message': 'Order updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/orders/<int:order_id>', methods=['DELETE'])
def remove_order(order_id):
    try:
        delete_order(order_id)
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Feedback endpoints
@api_bp.route('/api/feedback', methods=['GET'])
def get_all_feedback():
    try:
        conn = get_db_connection()
        feedback = conn.execute('SELECT * FROM feedback').fetchall()
        conn.close()
        return jsonify([dict(f) for f in feedback]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/feedback', methods=['POST'])
def create_feedback():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['name', 'email', 'message']):
            return jsonify({'error': 'All fields are required'}), 400
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)',
            (data['name'], data['email'], data['message'])
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Feedback submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/feedback/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    """
    Видалення одного відгуку за ID
    """
    try:
        conn = get_db_connection()
        # Перевіряємо чи існує відгук
        feedback = conn.execute('SELECT * FROM feedback WHERE id = ?', (feedback_id,)).fetchone()
        
        if not feedback:
            return jsonify({'error': 'Feedback not found'}), 404
            
        conn.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Feedback deleted successfully',
            'deleted_id': feedback_id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500