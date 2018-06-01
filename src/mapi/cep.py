# -*- coding: utf-8 -*-

# Standard
import json

# 3rd-party
from mapi import requests


__endpoint__ = 'http://www.viacep.com.br/ws'
__datatype__ = 'json'


class CEP:
    @staticmethod
    def format(response):
        return {
            'street': response['logradouro'],
            'district': response['bairro'],
            'city': response['localidade'],
            'state': response['uf']
        }

    @staticmethod
    def validate(cep):
        return cep.isdigit() and len(cep) is 8

    @staticmethod
    def query(cep):
        if not CEP.validate(cep):
            return None

        req_url = '{0}/{1}/{2}'.format(
            __endpoint__, cep, __datatype__
        )

        res = requests.get(req_url)
        if res.status_code is not 200:
            return None

        return CEP.format(json.loads(res.text))
