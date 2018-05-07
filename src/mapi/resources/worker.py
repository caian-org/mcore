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
from .person import PersonAuth


class WorkerNew(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass


class WorkerRecord(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def delete(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass

    def get(self, worker_id):
        """
        --- TODO: DOCUMENTATION ---
        """

        payload = request.get_json()

        if not Authenticator.check_struct(payload, ['auth']):
            return response.bad_request

        auth  = payload['auth']
        token = auth.get('token')

        if not token:
            return response.bad_request

        if not Authenticator.verify_token(token):
            return response.forbidden

        schema = WorkerSchema()
        worker = Worker.query.get(worker_id)

        data = schema.dump(worker).data
        return response.SUCCESS(200, data)

    def put(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass


class WorkerAuth(PersonAuth):
    """
    --- TODO: DOCUMENTATION ---
    """

    entity = Worker
