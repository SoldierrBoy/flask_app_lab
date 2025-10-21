from flask import Flask

app = Flask(__name__)

# --- РЕЄСТРАЦІЯ BLUEPRINTS ---

# 1. Реєструємо Blueprint для 'users'
from app.users.views import users_bp
app.register_blueprint(users_bp, url_prefix='/users')

# 2. Реєструємо Blueprint для 'products'
from app.products.views import products_bp
app.register_blueprint(products_bp, url_prefix='/products')

app.secret_key = 'a_very_secret_and_long_random_string'

# Імпортуємо основні маршрути (resume, contacts)
from app import views