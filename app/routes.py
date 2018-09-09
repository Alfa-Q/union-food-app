"""
routes.py
------------
Webpage navigation.
"""

from flask import render_template, flash, redirect, url_for
from app import app, mongo
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user
from app.user import User

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Homepage')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("User is already authenticated!")
        return redirect('/')
    else:
        print("User is not authenticated.")

    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))

        results = mongo.db.Users.find_one({'email': form.email.data})
        user = User(form.email.data, results.get('_id'))

        print(results)

        if not results is None:
            # Validate password
            valid_user = User.check_password(results.get('password_hash'), form.password.data)

            if valid_user:
                login_user(user, remember=form.remember_me.data)
                print("User logged in!")
                return redirect('/')

        
    return render_template('login.html', title='Login', form=form)

@app.route('/union')
def union():
    return render_template('locations/union.html', title='Union')

@app.route('/lassonde')
def lassonde():
    return render_template('locations/lassonde.html', title='Lassonde')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        flash('Registered!')
        return redirect('/')
    else:
        flash('Issue with registration')
    return render_template('register.html', title='Register', form=RegisterForm())

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')