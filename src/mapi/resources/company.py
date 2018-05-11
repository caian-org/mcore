# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

# Database connection
from . import db

# Worker model
from . import Company

# Worker datatype schema
from . import CompanySchema

# HTTP-related
from . import (Resource, request, response)

# Form/JSON data authenticator
from .auth import Authenticator

# Authentication logic
from .person import (PersonAuth, PersonRecord)


class CompanyAuth(PersonAuth):
    """
    --- TODO: DOCUMENTATION ---
    """

    entity = Company


class CompanyNew(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass


class CompanyRecord(PersonRecord):
    """
    --- TODO: DOCUMENTATION ---
    """
    entity = Company
    schema = CompanySchema

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


class CompanyProposals(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """
    pass
