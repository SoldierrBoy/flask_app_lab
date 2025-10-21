from flask import Flask

# Створюємо екземпляр нашого додатку
app = Flask(__name__)

# Імпортуємо наші маршрути (views) в кінці,
# щоб уникнути циклічних імпортів
from app import views