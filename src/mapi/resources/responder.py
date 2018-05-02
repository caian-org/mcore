# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""


class Response:
    """
    --- TODO: DOCUMENTATION ---
    """
    @staticmethod
    def SUCCESS(code, data):
        """
        --- TODO: DOCUMENTATION ---
        """
        response = {}
        response['code'] = code
        response['data'] = data
        response['status'] = 'Success'

        return response, code

    @staticmethod
    def FAIL(code, error):
        """
        --- TODO: DOCUMENTATION ---
        """
        response = {}
        response['code'] = code
        response['error'] = error
        response['status'] = 'Error'

        return response, code
