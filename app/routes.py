"""
routes.py
------------
Webpage navigation.
"""

from app import app

@app.route('/')
def index():
    return "Homepage"
