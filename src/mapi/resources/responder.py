# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from . import Formatter


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

    @property
    def internal_server_error(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        return Response.FAIL(500, 'Erro interno do servidor.')

    def address_created(self, uid):
        """
        --- TODO: DOCUMENTATION ---
        """
        data = {}
        data['id'] = uid
        data['uri'] = Formatter.gen_route('addresses/' + uid)

        return Response.SUCCESS(201, data)


response = Response()
