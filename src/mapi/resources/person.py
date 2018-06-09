# -*- coding: utf-8 -*-

# ...
from . import Person

# ...
from . import PersonSchema

# ...
from . import Resource
from . import request
from . import response

# ...
from .auth import Validator


class PersonAuth(Resource):
    entity = Person

    @staticmethod
    def authenticate(payload):
        """
        Método de autenticação de token
        """
        if not Validator.check_struct(payload, ['auth']):
            return False, response.bad_request

        auth = payload['auth']
        token = auth.get('token')

        if not token:
            return False, response.bad_request

        if not Validator.verify_token(token):
            return False, response.forbidden

        return True, None

    def get(self):
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
    entity = Person
    schema = PersonSchema

    def new(self, **kwargs):
        return self.entity(**kwargs)


class PersonRecord(Resource):
    entity = Person
    schema = PersonSchema

    def delete(self):
        pass

    def get(self, uid):
        payload = request.get_json()
        success, result = PersonRecord.authenticate(payload)

        if not success:
            return result

        person = self.entity.query.get(uid)

        data = self.schema().dump(person).data
        return response.SUCCESS(200, data)

    def put(self):
        pass
