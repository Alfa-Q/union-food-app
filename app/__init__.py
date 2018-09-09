"""
__init__.py
--------------------
Flask application instance.
"""

from flask import Flask
from flask_pymongo import PyMongo
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.config["MONGO_URI"] = "mongodb://localhost:27017/UEat"
mongo = PyMongo(app)


from app import routes
