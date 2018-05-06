# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from . import Worker
from . import (Resource, request, response)


class WorkerRecord(Resource):
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

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass

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
        email = request.form.get('email')
        passw = request.form.get('password')

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
