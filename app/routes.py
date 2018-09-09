"""
routes.py
------------
Webpage navigation.
"""

from flask import render_template, flash, redirect, url_for
from app import app, mongo
from app.forms import LoginForm, RegisterForm, AccountForm
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
        return redirect('/union')
    else:
        print("User is not authenticated.")

    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))

        results = mongo.db.Users.find_one({'email': form.email.data})

        print(results)

        if not results is None:
            user = User(results.get('first_name'), results.get('last_name'), form.email.data, results.get('_id'))
            # Validate password
            valid_user = User.check_password(results.get('password_hash'), form.password.data)

            if valid_user:
                login_user(user, remember=form.remember_me.data)
                print("User logged in!")
                return redirect('/union')

        
    return render_template('login.html', title='Login', form=form)

@app.route('/union')
def union():
    restaurants = mongo.db.UnionFood.find()
    return render_template('locations/union.html', title='Union', restaurants=restaurants)

@app.route('/lassonde')
def lassonde():
    return render_template('locations/lassonde.html', title='Lassonde')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Only display the webpage if the user is logged in. """
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))

    flash('Issue with registration')
    return render_template('register.html', title='Register', form=RegisterForm())

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/account')
def account():
    """ Only display the webpage if the user is logged in. """
    if current_user.is_authenticated:
        return render_template('account.html', title='Account', form=AccountForm())
    return redirect(url_for('login'))

@app.route('/payment')
def payments():
    return render_template('payments.html', title='Payment')

@app.route('/panda-express')
def panda():
    food_items = mongo.db.PandaExpressFood.find()
    return render_template('restaurants/panda-express.html', title='Panda Express', items=food_items)