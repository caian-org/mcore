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

# Authentication logic
from .person import (PersonAuth, PersonRecord, PersonNew)


class WorkerAuth(PersonAuth):
    """
    --- TODO: DOCUMENTATION ---
    """

    entity = Worker


class WorkerNew(PersonNew):
    """
    --- TODO: DOCUMENTATION ---
    """

    entity = Worker
    schema = WorkerSchema


class WorkerRecord(PersonRecord):
    """
    --- TODO: DOCUMENTATION ---
    """
    entity = Worker
    schema = WorkerSchema


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
