"""
forms.py
------------
Webpage forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder":"Email Address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder":"Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PaymentForm(FlaskForm):
    cardnumber = StringField('Card Number', validators=[DataRequired()])
    cardname = StringField('Name on Card', validators=[DataRequired()])
    cardcode = StringField('CVC', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        results = mongo.db.Users.find_one({'email': self.email.data})
        print("IN VALIDATE")
        if results is None:
            #User isn't in DB, add user
            if self.password.data == self.password_confirm.data:
                hash = generate_password_hash(self.password.data)
                mongo.db.Users.insert({'email':self.email.data, 'password_hash': hash})
                return True
            else:
                return False #Passwords do not match
        else:
            return False #Username already exists
