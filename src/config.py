# -*- coding: utf-8 -*-

import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


from mapi import Faker
_fake = Faker()


class Config:
    PORT = 80
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = _fake.password(length=128,
                                special_chars=True,
                                digits=True,
                                upper_case=True,
                                lower_case=True)


class Production(Config):
    pass


class Development(Config):
    PORT = 8080
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')


config = Production
if os.environ.get('TEST_ENVIRON'):
    config = Development
