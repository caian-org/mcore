#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard libraries
import sys
import unittest
from os import path
from datetime import datetime

# 3rd-party libraries
import requests

# Parent directory "injection"
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# Modules
from mapi import db
from mapi import app

# Models
from mapi.models import Address
from mapi.models import Company
from mapi.models import Item
from mapi.models import Vehicle
from mapi.models import Worker
from mapi.models import Proposal
from mapi.models import Offer

# Relations
from mapi.models import CompanyHasAddresses
from mapi.models import WorkerHasAddresses

# Utilitaries
from mapi import Faker
from mapi import Formatter

# Flask configurations
from mapi import config


class Fake:
    def __init__(self):
        self._brf = Faker('pt_BR')
        self._usf = Faker('en_US')

    @property
    def telephone(self):
        return self._brf.phone_number()\
            .replace('(', '')\
            .replace(')', '')\
            .replace(' ', '')\
            .replace('-', '')\
            .replace('+55', '')

    @property
    def password(self):
        return self._usf.password(
            length=32,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )

    @property
    def vehicle(self):
        vehicle = {}

        vehicle['year'] = self._brf.year()
        vehicle['brand'] = self._usf.company()
        vehicle['plate'] = self._brf.license_plate()
        vehicle['model'] = 'Modelo {0}'.format(self._usf.city_prefix())

        return vehicle

    @property
    def address(self):
        address = {}

        address['number'] = self._brf.building_number()
        address['postcode'] = self._brf.postcode().replace('-', '')
        address['complement'] = 'Sala {0}'.format(self._brf.random_uppercase_letter())

        return address

    @property
    def birthday(self):
        birthday = self._brf.date_this_century(before_today=True)
        b_year = birthday.year
        c_year = datetime.now().year

        if (c_year - b_year) < 21:
            b_year = b_year - (21 - (c_year - b_year))

        return '{0}-{1}-{2}'.format(birthday.day, birthday.month, b_year)

    @property
    def person(self):
        data = {}

        data['rg'] = self._brf.numerify(text='#' * 9)
        data['cpf'] = self._brf.numerify(text='#' * 11)
        data['name'] = self._brf.name()
        data['email'] = self._brf.email()
        data['licenseId'] = self._brf.numerify(text='#' * 11)
        data['licenseType'] = self._brf.random_uppercase_letter()

        data['gender'] = 'M'
        data['password'] = self.password
        data['birthday'] = self.birthday
        data['telephone'] = self.telephone

        return data

    @property
    def worker(self):
        payload = {}

        payload['data'] = self.person
        payload['data']['vehicle'] = self.vehicle
        payload['data']['address'] = self.address

        return payload


class TestRoutes(unittest.TestCase):
    fake = Fake()

    worker_cred = []
    company_cred = []

    @property
    def worker_profile(self):
        return self.__class__.fake.worker

    @property
    def company_profile(self):
        return self.__class__.fake.company

    def inc_worker_cred(self, credential):
        self.__class__.worker_cred.append(credential)

    def inc_company_cred(self, credential):
        self.__class__.company_cred.append(credential)

    def ins_worker_token(self, index, token):
        self.__class__.worker_cred[index]['token'] = token

    def ins_company_token(self, index, token):
        self.__class__.company_cred[index]['token'] = token

    def gen_url(self, resource):
        return '{0}:{1}{2}'.format(
            'http://localhost', config.PORT,
            Formatter.gen_route(resource)
        )

    def test_a_worker_creation(self):
        def gen_worker_profiles():
            for i in range(0, 20):
                profile = self.worker_profile

                def get_cred():
                    cred = {}
                    cred['email'] = profile['data']['email']
                    cred['password'] = profile['data']['password']
                    return cred

                self.inc_worker_cred(get_cred())

                result = requests.post(
                    self.gen_url('workers'),
                    json=profile
                )

                if not result.status_code == 201:
                    return False

            return True

        self.assertEqual(gen_worker_profiles(), True)

    def test_b_worker_authentication(self):
        def authenticate_workers():
            for i, worker in enumerate(self.__class__.worker_cred):
                result = requests.post(self.gen_url('workers/auth'), json={
                    'email': worker['email'],
                    'password': worker['password']
                })

                if not result.status_code == 200:
                    return False

                response = result.json()
                self.ins_worker_token(i, response['data']['token'])

            return True

        self.assertEqual(authenticate_workers(), True)


if __name__ == '__main__':
    unittest.main()
