# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from . import Person


class Authenticator:
    @staticmethod
    def check_struct(payload):
        elements = [ payload.get('auth'), payload.get('data') ]

        for element in elements:
            if not isinstance(element, dict):
                return False

        return True

    @staticmethod
    def check_payload(params):
        for param in params:
            if not param:
                return False

        return True

    @staticmethod
    def verify_token(entity, token):
        if entity not in ['worker', 'company']:
            return False

        return Person.verify_token(token)
