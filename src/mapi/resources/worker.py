# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from . import Worker
from . import (Resource, request, response)

from . import BadRequest


class WorkerAuthentication(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        try:
            email = request.form['email']
            passw = request.form['password']
        except BadRequest as error:
            return response.FAIL(400, error.description)

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
