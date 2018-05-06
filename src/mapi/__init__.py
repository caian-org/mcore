# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

__parent_resource__ = 'api'
__version__ = 'v1'


# Standard library
import os

# Modules
from mapi.utils import Exit

# 3rd-party libraries
try:
    from faker import Faker

    # Flask itself
    from flask import Flask, request

    # REST API abstraction layer
    from flask_restful import (Api as Restful, Resource)

    # ORM-related
    from flask_migrate import Migrate
    from flask_sqlalchemy import SQLAlchemy

    # Security modules (login-related)
    from werkzeug.security import (generate_password_hash as gen_phash,
                                   check_password_hash as check_phash)

    from werkzeug.exceptions import BadRequest

    # Security modules (token-related)
    from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                              BadSignature, SignatureExpired)

    # Mail service API
    import pycep_correios as cep_api
    from pycep_correios.excecoes import (Timeout, FalhaNaConexao,
                                         MultiploRedirecionamento)

except ImportError as error:
    Exit.with_fail('Impossible to import 3rd-party libraries\n'
                   'Latest traceback: {0}' . format(error.args[0]))

# Very long (and secret) key
from mapi.secret import SECRET_KEY


# What kind of configuration should be used?
if os.environ.get('TEST_ENVIRON'):
    from config import Development as Config

else:
    from config import Production as Config


Config.SECRET_KEY = SECRET_KEY

app = Flask(__name__)
app.config.from_object(Config)

rapi = Restful(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
