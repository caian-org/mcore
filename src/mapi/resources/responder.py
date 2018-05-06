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

    @property
    def incorrect_email_or_password(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        return Response.FAIL(404, 'E-mail ou senha incorretos.')

    @property
    def bad_request(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        return Response.FAIL(400, 'Requisição inválida.')


response = Response()
