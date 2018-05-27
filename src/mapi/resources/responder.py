# -*- coding: utf-8 -*-

from . import Formatter


class Response:
    @staticmethod
    def SUCCESS(code, data):
        response = {}
        response['code'] = code
        response['data'] = data
        response['status'] = 'Success'

        return response, code

    @staticmethod
    def FAIL(code, error):
        response = {}
        response['code'] = code
        response['error'] = error
        response['status'] = 'Error'

        return response, code

    @property
    def bad_request(self):
        return Response.FAIL(400, 'Requisição inválida.')

    @property
    def incorrect_email_or_password(self):
        return Response.FAIL(403, 'E-mail ou senha incorretos.')

    @property
    def forbidden(self):
        return Response.FAIL(403, 'Acesso negado.')

    @property
    def not_found(self):
        return Response.FAIL(404, 'Recurso não encontrado.')

    @property
    def internal_server_error(self):
        return Response.FAIL(500, 'Erro interno do servidor.')

    def created(self, resource, uid):
        data = {}
        data['id'] = uid
        data['uri'] = Formatter.gen_route('{0}/{1}'.format(resource, uid))

        return Response.SUCCESS(201, data)


response = Response()
