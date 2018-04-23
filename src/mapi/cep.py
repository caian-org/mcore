# -*- coding: utf-8 -*-

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from mapi.utils import Exit

try:
    import pycep_correios as cep_api
    from pycep_correios.excecoes import (Timeout,
                                         FalhaNaConexao,
                                         MultiploRedirecionamento)

except ImportError as error:
    Exit.with_fail('Impossible to import 3rd-party libraries\n'
                   'Latest traceback: {0}' . format(error.args[0]))


class CEP:
    """
    --- TODO: DOCUMENTATION ---
    """
    @staticmethod
    def format(response):
        """
        --- TODO: DOCUMENTATION ---
        """
        return {
            'street': response['end'],
            'district': response['bairro'],
            'city': response['cidade'],
            'state': response['uf']
        }

    @staticmethod
    def validate(cep):
        """
        --- TODO: DOCUMENTATION ---
        """
        return cep_api.validar_cep(cep)

    @staticmethod
    def query(cep):
        """
        --- TODO: DOCUMENTATION ---
        """
        if not CEP.validate(cep):
            return False

        try:
            return CEP.format(cep_api.consultar_cep(cep))

        except (Timeout, FalhaNaConexao, MultiploRedirecionamento):
            return False
