"""
routes.py
------------
Webpage navigation.
"""

from flask import render_template, flash, redirect, url_for
from app import app, mongo
from app.forms import LoginForm, RegisterForm, AccountForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Only display the webpage if the user is logged in. """
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        login_user(user, remember=form.remember_me.data)
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

@app.route('/union')
def union():
    return render_template('locations/union.html', title='Union')

@app.route('/lassonde')
def lassonde():
    return render_template('locations/lassonde.html', title='Lassonde')

@app.route('/payment')
def payments():
    return render_template('payments.html', title='Payment')

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        results = mongo.db.Users.find_one({'email': form.email.data})
        if results:
            user = User(results.get('first_name'), results.get('last_name'), form.email.data, results.get('_id'))
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        print('not authenticated')
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        print('No user found for reset token')
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        mongo.db.Users.find_one_and_update({'email':user.email}, {'$set': {'password_hash':form.hash}})
        flash('Your password has been successfully updated.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)