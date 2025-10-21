from flask import Blueprint, render_template, request, redirect, url_for

# Створюємо Blueprint з назвою 'users'
# 'template_folder='templates'' вказує, де шукати шаблони для цього blueprint
users_bp = Blueprint('users', __name__, template_folder='templates')

# Маршрути, що належать цьому Blueprint
# Замість @app.route використовуємо @users_bp.route
@users_bp.route("/hi/<string:name>")
def greetings(name):
    # Отримуємо параметр 'age' з URL, якщо він є
    age = request.args.get("age")
    return render_template("users/hi.html", name=name.upper(), age=age)

@users_bp.route("/admin")
def admin():
    # Перенаправляємо на сторінку greetings з конкретними параметрами
    return redirect(url_for("users.greetings", name="Administrator"))