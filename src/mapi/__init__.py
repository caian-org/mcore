# -*- coding: utf-8 -*-

__parent_resource__ = 'api'
__version__ = 'v1'


# Utils
from mapi.utils import Exit
from mapi.utils import Formatter


#   ____       _                    _
#  |__ /_ _ __| |___ _ __  __ _ _ _| |_ _  _
#   |_ \ '_/ _` |___| '_ \/ _` | '_|  _| || |
#  |___/_| \__,_|   | .__/\__,_|_|  \__|\_, |
#                   |_|                 |__/
try:
    # Fake data generator
    from faker import Faker

    # Flask-related
    from flask import Flask, request

    # REST API abstraction layer for Flask
    from flask_restful import Resource
    from flask_restful import Api as Restful

    # ORM-related
    from flask_migrate import Migrate
    from sqlalchemy.orm import joinedload
    from flask_sqlalchemy import SQLAlchemy
    from flask_marshmallow import Marshmallow

    # Security modules (login-related)
    from werkzeug.security import generate_password_hash as gen_phash
    from werkzeug.security import check_password_hash as check_phash

    # Security modules (token-related)
    from itsdangerous import BadSignature
    from itsdangerous import SignatureExpired
    from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

    # Correios API
    import pycep_correios as cep_api
    from pycep_correios.excecoes import Timeout
    from pycep_correios.excecoes import FalhaNaConexao
    from pycep_correios.excecoes import MultiploRedirecionamento

except ImportError as error:
    Exit.with_fail('Impossible to import 3rd-party libraries\n'
                   'Latest traceback: {0}' . format(error.args[0]))

# Configurations & definitions
from config import config


#       _     _        _
#   ___| |__ (_)___ __| |_ ___
#  / _ \ '_ \| / -_) _|  _(_-<
#  \___/_.__// \___\__|\__/__/
#          |__/
#
app = Flask(__name__)
app.config.from_object(config)

db   = SQLAlchemy(app)
mars = Marshmallow(app)
migr = Migrate(app, db)
rapi = Restful(app)
