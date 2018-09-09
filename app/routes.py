"""
routes.py
------------
Webpage navigation.
"""

from flask import render_template, flash, redirect
from app import app, mongo
from app.forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    return render_template("index.html")

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