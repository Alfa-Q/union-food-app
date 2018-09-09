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
app.config["MONGO_URI"] = "mongodb+srv://admin:josh12345@cluster0-ghotr.gcp.mongodb.net/UEat"
# 
mongo = PyMongo(app)


from app import routes
