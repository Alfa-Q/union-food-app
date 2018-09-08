"""
config.py
------------
Secret key configuration.
"""

import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key123'