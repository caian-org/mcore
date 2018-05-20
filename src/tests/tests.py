#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

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
from mapi import db, app
from mapi.models import (Address, Company, Item, Vehicle, Worker,
                         CompanyHasAddresses, WorkerHasAddresses,
                         Proposal, Offer)

# Utilitaries
from mapi import Faker, Formatter

# Flask configurations
from mapi import config

br_fake = Faker('pt_BR')
us_fake = Faker('en_US')


class Record:
    @staticmethod
    def gen_person_payload():
        payload = {}

        tel = br_fake.phone_number()\
            .replace('(', '')\
            .replace(')', '')\
            .replace(' ', '')\
            .replace('-', '')\
            .replace('+55', '')

        psw = br_fake.password(length=32,
                               special_chars=True,
                               digits=True,
                               upper_case=True,
                               lower_case=True)

        birthday = br_fake.date_this_century(before_today=True)
        b_year = birthday.year
        c_year = datetime.now().year

        if (c_year - b_year) < 21:
            b_year = b_year - (21 - (c_year - b_year))

        birthday = '{0}-{1}-{2}'.format(birthday.day,
                                        birthday.month,
                                        b_year)

        data = {}
        data['name']        = br_fake.name()
        data['telephone']   = tel
        data['email']       = br_fake.email()
        data['password']    = psw
        data['rg']          = br_fake.numerify(text='#' * 9)
        data['cpf']         = br_fake.numerify(text='#' * 11)
        data['gender']      = 'M'
        data['birthday']    = birthday
        data['licenseId']   = br_fake.numerify(text='#' * 11)
        data['licenseType'] = br_fake.random_uppercase_letter()

        vehicle = {}
        vehicle['model'] = 'Modelo ' + us_fake.city_prefix()
        vehicle['brand'] = us_fake.company()
        vehicle['plate'] = br_fake.license_plate()
        vehicle['year']  = br_fake.year()

        address = {}
        address['number']   = br_fake.building_number()
        address['postcode'] = br_fake.postcode().replace('-', '')
        address['complement'] = 'Sala ' + br_fake.random_uppercase_letter()

        payload['data'] = data
        payload['data']['vehicle'] = vehicle
        payload['data']['address'] = address

        return payload


class TestRoutes(unittest.TestCase):
    """
    --- TODO: DOCUMENTATION ---
    """
    def gen_url(self, resource):
        """
        --- TODO: DOCUMENTATION ---
        """
        return '{0}:{1}{2}'.format(
            'http://localhost', config.PORT,
            Formatter.gen_route(resource)
        )

    def test_a_worker_creation(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        def iterator():
            for i in range(0, 20):
                payload = Record.gen_person_payload()
                result = requests.post(self.gen_url('workers'), json=payload)

                if not result.status_code == 201:
                    return False

            return True

        status = iterator()
        self.assertEqual(status, True)

    def test_b_company_creation(self):
        pass


if __name__ == '__main__':
    unittest.main()
