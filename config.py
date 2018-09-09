"""
config.py
------------
Secret key configuration.
"""

import os


class Config(object):
    SECRET_KEY  = os.environ.get('SECRET_KEY') or 'super_secret_key123'
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS  = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['alfakyuu@gmail.com', 'ryanmilleris@yahoo.com', 'slkrstyen@gmail.com']