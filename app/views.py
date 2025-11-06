from flask import render_template, flash, redirect, url_for, Blueprint
from app.forms import ContactForm
import logging


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def resume():
    return render_template('resume.html', title="My Resume")

@main_bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        logging.info(f"New contact submission from {name} ({email})")
        flash(f'Thanks, {name}! Your message has been sent.', 'success')
        return redirect(url_for('main.contacts'))

    return render_template('contacts.html', title="Contacts", form=form)