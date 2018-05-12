# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

# Standard
import urllib3

# 3rd-party
from mapi import cep_api
from mapi import (Timeout, FalhaNaConexao, MultiploRedirecionamento)

# Disables the "InsecureRequestWarning" warning in urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
