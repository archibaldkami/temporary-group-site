from flask import Blueprint, render_template, redirect, url_for, request
from models import get_db_connection, get_orders, get_order_details, update_order_status, delete_order

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin():
    conn = get_db_connection()
    feedback = conn.execute('SELECT * FROM feedback').fetchall()
    conn.close()
    orders = get_orders()
    return render_template('admin.html', feedback=feedback, orders=orders)

@admin_bp.route('/admin/delete_feedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM feedback WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/order/<int:order_id>')
def order_details(order_id):
    order, items = get_order_details(order_id)
    return render_template('order_details.html', order=order, items=items)

@admin_bp.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
def update_order(order_id):
    status = request.form['status']
    update_order_status(order_id, status)
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/delete_order/<int:order_id>', methods=['POST'])
def delete_order_route(order_id):
    delete_order(order_id)
    return redirect(url_for('admin.admin'))