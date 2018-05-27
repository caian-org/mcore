# -*- coding: utf-8 -*-

# Standard
import urllib3

# 3rd-party
from mapi import cep_api
from mapi import (Timeout, FalhaNaConexao, MultiploRedirecionamento)

# Disables the "InsecureRequestWarning" warning in urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CEP:
    @staticmethod
    def format(response):
        return {
            'street': response['end'],
            'district': response['bairro'],
            'city': response['cidade'],
            'state': response['uf']
        }

    @staticmethod
    def validate(cep):
        return cep_api.validar_cep(cep)

    @staticmethod
    def query(cep):
        if not CEP.validate(cep):
            return False

        try:
            return CEP.format(cep_api.consultar_cep(cep))

        except (Timeout, FalhaNaConexao, MultiploRedirecionamento):
            return False
