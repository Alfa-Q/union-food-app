"""
routes.py
------------
Webpage navigation.
"""

from flask import render_template, url_for
from app import app
from app.forms import LoginForm, RegisterForm


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Homepage")

@app.route('/login')
def login():
    return render_template('login.html', title='Login', form=LoginForm())

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Registered!')
        return redirect(url_for('/index'))
    return render_template('register.html', title='Register', form=RegisterForm())
