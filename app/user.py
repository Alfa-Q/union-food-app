"""
user.py
------------
User class.
"""
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import app, login, mongo
from hashlib import md5
from time import time
import jwt

class User(UserMixin):

    def __init__(self, first, last, email, id):
        self.first_name = first
        self.last_name = last
        self.email = email
        self.id = str(id)

    @staticmethod
    def check_password(hash, password):
        return check_password_hash(hash, password)

    def set_id(self, id):
        self.id = id

    # Using email instead of actual id
    def get_id(self):
        return self.email

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password':self.email, 'exp':time()+expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], 
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return load_user(id)

    
@login.user_loader
def load_user(email):
    u = mongo.db.Users.find_one({"email": email})
    if not u:
        return None
    return User(u['first_name'], u['last_name'], u['email'], str(u['_id']))


