# -*- coding: utf-8 -*-

from . import config
from . import Person


class Authenticator:
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
