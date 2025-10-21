from flask import render_template
from app import app

@app.route('/')
def resume():
    return render_template('resume.html', title="My Resume")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Contact Me")