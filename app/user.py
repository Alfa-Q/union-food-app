"""
user.py
------------
User class.
"""
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login, mongo

class User(UserMixin):

    def __init__(self, email, id):
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

    
@login.user_loader
def load_user(email):
    u = mongo.db.Users.find_one({"email": email})
    if not u:
        return None
    return User(u['email'], str(u['_id']))


