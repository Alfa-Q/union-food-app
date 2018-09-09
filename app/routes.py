"""
routes.py
------------
Webpage navigation.
"""

from flask import render_template
from app import app
from app.forms import LoginForm


@app.route('/')
def index():
    return render_template("index.html", title='Homepage')

@app.route('/login')
def login():
    return render_template('login.html', title='Login', form=LoginForm())

@app.route('/test')
def test():
    return render_template('test.html', title='Test Page')

