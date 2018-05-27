# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from . import config
from . import Person


class Authenticator:
    """
    --- TODO: DOCUMENTATION ---
    """

    @staticmethod
    def check_struct(payload, elements):
        """
        --- TODO: DOCUMENTATION ---
        """

        for element in elements:
            if not isinstance(payload.get(element), dict):
                return False

        return True

    @staticmethod
    def check_payload(params):
        """
        --- TODO: DOCUMENTATION ---
        """

        for param in params:
            if param is None:
                return False

        return True

    @staticmethod
    def verify_token(token):
        """
        --- TODO: DOCUMENTATION ---
        """

        if config.DEBUG:
            if token == 'master_token':
                return True

        return Person.verify_token(token)
