"""
user.py
------------
User class.
"""
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login, mongo
from hashlib import md5

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

    
@login.user_loader
def load_user(email):
    u = mongo.db.Users.find_one({"email": email})
    if not u:
        return None
    return User(u['first_name'], u['last_name'], u['email'], str(u['_id']))


