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
    # Flask itself
    from flask import Flask

    # REST API abstraction layer
    from flask_restful import Api

    # ORM-related
    from flask_migrate import Migrate
    from flask_sqlalchemy import SQLAlchemy

except ImportError as error:
    Exit.with_fail('Impossible to import 3rd-party libraries\n'
                   'Latest traceback: {0}' . format(error.args[0]))

# What kind of configuration should be used?
if os.environ.get('TEST_ENVIRON'):
    from config import Development as Config

else:
    from config import Production as Config


app = Flask(__name__)
app.config.from_object(Config)

rapi = Api(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
