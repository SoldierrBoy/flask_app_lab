from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from .models import User
from .forms import LoginForm, RegistrationForm  # <-- Беремо форми з папки users

users_bp = Blueprint('users', __name__, template_folder='templates')


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # 1. Хешуємо пароль
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # 2. Створюємо юзера
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)

        # 3. Зберігаємо
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', title='Register', form=form)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        # Шукаємо юзера в БД
        user = db.session.scalar(db.select(User).where(User.username == form.username.data))

        # Перевіряємо пароль через bcrypt
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome back, {user.username}!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.profile'))
        else:
            flash('Login failed. Please check identifier and password.', 'danger')

    return render_template('users/login.html', title='Login', form=form)
@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    return render_template('users/profile.html', title='Profile', user=current_user)


@users_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('users.login'))


@users_bp.route('/set-theme/<theme>')
def set_theme(theme):
    if theme in ['light', 'dark']:
        response = make_response(redirect(request.referrer or url_for('users.profile')))
        response.set_cookie('theme', theme, max_age=60 * 60 * 24 * 30)
    else:
        response = make_response(redirect(request.referrer or url_for('users.profile')))
    return response

@users_bp.route('/users')
@login_required
def users_list():
    users = db.session.scalars(db.select(User).order_by(User.id)).all()
    return render_template('users/users_list.html', title='Users List', users=users, count=len(users))