"""
forms.py
------------
Webpage forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app import mongo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
    

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        results = mongo.db.Users.find_one({'email': self.email})
        if results is None:
            #User isn't in DB, add user
            if password == password_confirm:
                hash = generate_password_hash(self.password)
                mongo.db.Users.insert({'email':self.email, 'password_hash': hash})
                return True
            else:
                return False #Passwords do not match
        else:
            return False #Username already exists
