from flask import Blueprint, render_template, request, jsonify
from models import get_db_connection

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)',
                     (name, email, message))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success"}), 200
    
    return render_template('feedback.html')