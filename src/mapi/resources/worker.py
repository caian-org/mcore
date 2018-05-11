# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

# Database connection
from . import db

# Worker model
from . import Worker

# Worker datatype schema
from . import WorkerSchema

# HTTP-related
from . import (Resource, request, response)

# Form/JSON data authenticator
from .auth import Authenticator

# Authentication logic
from .person import (PersonAuth, PersonRecord)


class WorkerAuth(PersonAuth):
    """
    --- TODO: DOCUMENTATION ---
    """

    entity = Worker


class WorkerNew(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass


class WorkerRecord(PersonRecord):
    """
    --- TODO: DOCUMENTATION ---
    """
    entity = Worker
    schema = WorkerSchema

    def delete(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass

    def put(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass


class WorkerAddresses(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """
    pass


class WorkerVehicles(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """
    pass
