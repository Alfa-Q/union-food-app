"""
routes.py
------------
Webpage navigation.
"""

from flask import render_template, flash, redirect, url_for
from app import app, mongo
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Homepage")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Email is " + form.email.data)
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))

        # Generate the hash and check if email/hash in db
        hash = generate_password_hash(form.password.data)
        results = mongo.db.Users.find_one({'email': form.email.data})
        # Compare hash with password
        valid_user = check_password_hash(results.get('password_hash'), form.password.data)

        print(results)
        print(valid_user)

        if valid_user:
            return redirect('/')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        flash('Registered!')
        return redirect(url_for('/index'))
    else:
        flash('Issue with registration')
    return render_template('register.html', title='Register', form=RegisterForm())
