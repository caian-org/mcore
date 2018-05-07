# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

# Database connection
from . import db

# Worker model
from . import Vehicle

# HTTP-related
from . import (Resource, request, response)

# Form/JSON data authenticator
from .auth import Authenticator


class VehicleNew(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass


class VehicleRecord(Resource):
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
