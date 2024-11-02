from flask import Flask, render_template, session
from models import init_db
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Необхідно для роботи з сесіями

# Ініціалізація бази даних
init_db()

# Реєстрація блюпрінтів
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)