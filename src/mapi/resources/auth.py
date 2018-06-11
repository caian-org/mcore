# -*- coding: utf-8 -*-

from . import Person
from . import config
from . import response


class Validator:
    @staticmethod
    def check_struct(payload, elements):
        for element in elements:
            if not isinstance(payload.get(element), dict):
                return False

        return True

    @staticmethod
    def check_payload(params):
        for param in params:
            if param is None:
                return False

        return True

    @staticmethod
    def verify_token(token):
        if config.DEBUG:
            if token == 'master_token':
                return True

        return Person.verify_token(token)


class Authorizer:
    @staticmethod
    def validate(kind, payload, elements):
        if not payload:
            return True, response.bad_request

        # Verifica a estrutura da payload recebida
        if not Validator.check_struct(payload, elements):
            return True, response.bad_request

        # Verifica se o token é valido
        auth = payload['auth']
        token = auth.get('token')

        user_token = Validator.verify_token(token)
        if not user_token:
            return True, response.forbidden

        # Verifica se o token pertence ao tipo de usuário indicado
        if user_token['kind'] != kind and user_token['kind'] != 'any':
            return True, response.forbidden

        return False, None
