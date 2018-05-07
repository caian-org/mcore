# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

# Worker model
from . import Person

# HTTP-related
from . import (Resource, request, response)


class PersonAuth(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    entity = Person

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        payload = request.get_json()
        email = payload.get('email')
        passw = payload.get('password')

        if not email or not passw:
            return response.bad_request

        worker = self.entity.query.filter_by(email=email).all()
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
