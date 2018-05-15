# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

# Worker model
from . import Person

# Person datatype schema
from . import PersonSchema

# HTTP-related
from . import (Resource, request, response)

# Form/JSON data authenticator
from .auth import Authenticator


class PersonAuth(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    entity = Person

    @staticmethod
    def authenticate(payload):
        """
        Método de autenticação de token
        """
        if not Authenticator.check_struct(payload, ['auth']):
            return False, response.bad_request

        auth = payload['auth']
        token = auth.get('token')

        if not token:
            return False, response.bad_request

        if not Authenticator.verify_token(token):
            return False, response.forbidden

        return True, None

    def post(self):
        """
        Método de autenticação do usuário via email e senha (aka login)
        """
        payload = request.get_json()
        email = payload.get('email')
        passw = payload.get('password')

        if not email or not passw:
            return response.bad_request

        person = self.entity.query.filter_by(email=email).all()
        if not person:
            return response.incorrect_email_or_password

        person = person[0]
        valid_passw = person.verify_password(passw)
        if not valid_passw:
            return response.incorrect_email_or_password

        token = person.generate_token()

        data = {}
        data['token'] = token.decode('ascii')
        return response.SUCCESS(200, data)


class PersonNew(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """
    entity = Person
    schema = PersonSchema

    def new(self, **kwargs):
        """
        --- TODO: DOCUMENTATION ---
        """
        return self.entity(**kwargs)


class PersonRecord(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """
    entity = Person
    schema = PersonSchema

    def delete(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass

    def get(self, uid):
        """
        --- TODO: DOCUMENTATION ---
        """
        payload = request.get_json()
        success, result = PersonRecord.authenticate(payload)

        if not success:
            return result

        person = self.entity.query.get(uid)

        data = self.schema().dump(person).data
        return response.SUCCESS(200, data)

    def put(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass
