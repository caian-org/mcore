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


class WorkerAuth(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        payload = request.get_json()
        email = payload.get('email')
        passw = payload.get('password')

        if not email or not passw:
            return response.bad_request

        worker = Worker.query.filter_by(email=email).all()
        if not worker:
            return response.incorrect_email_or_password

        worker = worker[0]
        valid_passw = worker.verify_password(passw)
        if not valid_passw:
            return response.incorrect_email_or_password

        token = worker.generate_token()

        data = {}
        data['token'] = token.decode('ascii')
        return response.SUCCESS(200, data)
