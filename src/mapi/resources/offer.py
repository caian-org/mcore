# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

# Database connection
from . import db

# Worker model
from . import Offer

# HTTP-related
from . import (Resource, request, response)

# Form/JSON data authenticator
from .auth import Authenticator


class OfferNew(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass


class OfferRecord(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def delete(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass

    def get(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass

    def put(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass
