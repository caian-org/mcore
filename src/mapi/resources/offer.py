# -*- coding: utf-8 -*-

# Database connection
from . import db

# Worker model
from . import Offer

# HTTP-related
from . import (Resource, request, response)

# Form/JSON data authenticator
from .auth import Authenticator


class OfferNew(Resource):
    def post(self):
        pass


class OfferRecord(Resource):
    def delete(self):
        pass

    def get(self):
        pass

    def put(self):
        pass
