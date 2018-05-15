# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

# Database connection
from . import db

# Admin model
from . import Admin

# Admin datatype schema
from . import AdminSchema

# HTTP-related
from . import (Resource, request, response)

# Authentication logic
from .person import (PersonAuth, PersonRecord, PersonNew)


class AdminAuth(PersonAuth):
    """
    --- TODO: DOCUMENTATION ---
    """

    entity = Admin


class AdminNew(PersonNew):
    """
    --- TODO: DOCUMENTATION ---
    """

    entity = Admin
    schema = AdminSchema


class AdminRecord(PersonRecord):
    """
    --- TODO: DOCUMENTATION ---
    """
    entity = Admin
    schema = AdminSchema
