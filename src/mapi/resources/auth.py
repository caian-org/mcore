# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from . import Person


class Authenticator:
    """
    --- TODO: DOCUMENTATION ---
    """

    @staticmethod
    def check_struct(payload):
        """
        --- TODO: DOCUMENTATION ---
        """
        elements = [ payload.get('auth'), payload.get('data') ]

        for element in elements:
            if not isinstance(element, dict):
                return False

        return True

    @staticmethod
    def check_payload(params):
        """
        --- TODO: DOCUMENTATION ---
        """
        for param in params:
            if not param:
                return False

        return True

    @staticmethod
    def verify_token(token):
        """
        --- TODO: DOCUMENTATION ---
        """
        return Person.verify_token(token)
