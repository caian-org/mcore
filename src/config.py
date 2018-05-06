# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    PORT = 80
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = None


class Production(Config):
    pass


class Development(Config):
    PORT = 8080
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
