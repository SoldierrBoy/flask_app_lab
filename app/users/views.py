import os
import secrets
from PIL import Image
from datetime import datetime, UTC
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from .models import User
from .forms import LoginForm, RegistrationForm, UpdateAccountForm, ChangePasswordForm

users_bp = Blueprint('users', __name__, template_folder='templates')


@users_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(UTC)
        db.session.commit()



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)

    output_size = (128, 128)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
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
        user = db.session.scalar(db.select(User).where(User.username == form.username.data))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(request.args.get('next') or url_for('users.profile'))
        else:
            flash('Login failed. Check username and password.', 'danger')

    return render_template('users/login.html', title='Login', form=form)


@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_image = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('static', filename='images/' + current_user.profile_image)
    theme = request.cookies.get('theme', 'light')

    return render_template('users/profile.html', title='Profile',
                           image_file=image_file, form=form, theme=theme)


@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Unsuccessful. Please check your old password.', 'danger')

    return render_template('users/change_password.html', title='Change Password', form=form)


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
        return response
    return redirect(url_for('users.profile'))


@users_bp.route('/users')
@login_required
def users_list():
    users = db.session.scalars(db.select(User).order_by(User.id)).all()
    return render_template('users/users_list.html', title='Users List', users=users, count=len(users))