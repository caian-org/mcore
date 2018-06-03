#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Biblioteca padrão
import sys
import random
import unittest
from os import path
from datetime import datetime

# CEPs válidos de São Paulo
from postcodes import __valid_postcodes__

# Injeta o diretório superior para que "mapi" seja visível
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from mapi import Faker      # Gerador de dados falsos
from mapi import Formatter  # Formatador de rota de recurso REST
from mapi import config     # Objeto de configurações do programa
from mapi import requests   # Faz chamadas POST e GET (3rd-party)


class Fake:
    def __init__(self):
        self._brf = Faker('pt_BR')
        self._usf = Faker('en_US')

    @property
    def deadline(self):
        deadline = self._brf.future_date(end_date='+45d')
        return '{0}-{1}-{2}'.format(deadline.day, deadline.month, deadline.year)

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
        address['postcode'] = random.choice(__valid_postcodes__)
        address['complement'] = 'Sala {0}'.format(self._brf.random_uppercase_letter())

        return address

    @property
    def human(self):
        data = {}

        gender = self._brf.boolean(chance_of_getting_true=50)
        if gender:
            data['name'] = '{0} {1}'\
                .format(self._brf.first_name_male(), self._brf.last_name())
            data['gender'] = 'M'

        else:
            data['name'] = '{0} {1}'\
                .format(self._brf.first_name_female(), self._brf.last_name())
            data['gender'] = 'F'

        data['rg'] = self._brf.numerify(text='#' * 9)
        data['cpf'] = self._brf.numerify(text='#' * 11)
        data['email'] = self._brf.email()
        data['birthday'] = self.birthday()
        data['password'] = self.password
        data['telephone'] = self.telephone

        return data

    @property
    def worker(self):
        worker = self.human
        worker['licenseId'] = self._brf.numerify(text='#' * 11)
        worker['licenseType'] = self._brf.random_uppercase_letter()

        payload = {}
        payload['data'] = worker
        payload['data']['vehicle'] = self.vehicle
        payload['data']['address'] = self.address

        return payload

    @property
    def admin(self):
        admin = self.human
        admin['authorityLevel'] = '1'

        payload = {}
        payload['data'] = admin
        payload['data']['address'] = self.address

        return payload

    @property
    def company(self):
        company = {}
        company['name'] = self._usf.company()
        company['cnpj'] = self._usf.numerify(text='#' * 14)
        company['email'] = self._usf.company_email()
        company['opening'] = self.birthday(legal_age=False)
        company['password'] = self.password
        company['telephone'] = self.telephone

        payload = {}
        payload['data'] = company
        payload['data']['address'] = self.address

        return payload

    @property
    def item(self):
        item = {}
        item['title'] = self._brf.sentence(nb_words=2).replace('.', '')
        item['width'] = '{:.2f}'.format(random.uniform(0.1, 10.0))
        item['height'] = '{:.2f}'.format(random.uniform(0.1, 10.0))
        item['weight'] = '{:.2f}'.format(random.uniform(0.1, 10.0))
        item['fragile'] = self._brf.boolean(chance_of_getting_true=50)

        return item

    def birthday(self, legal_age=True):
        birthday = self._brf.date_this_century(before_today=True)
        b_year = birthday.year
        c_year = datetime.now().year

        min_age = 21
        if not legal_age:
            min_age = 3

        if (c_year - b_year) < min_age:
            b_year = b_year - (min_age - (c_year - b_year))

        return '{0}-{1}-{2}'.format(birthday.day, birthday.month, b_year)

    def proposal(self, company_uid, company_token, status):
        proposal = {}
        proposal['title'] = self._brf.sentence(nb_words=5).replace('.', '')
        proposal['status'] = status
        proposal['deadline'] = self.deadline
        proposal['companyUid'] = company_uid
        proposal['description'] = ''.join(
            str(p) for p in self._brf.paragraphs(nb=2)
        )

        items = []
        for _ in range(0, 5):
            items.append(self.item)

        auth = {}
        auth['token'] = company_token

        payload = {}
        payload['auth'] = auth
        payload['data'] = proposal
        payload['data']['items'] = items
        payload['data']['originAddress'] = self.address
        payload['data']['destinationAddress'] = self.address

        return payload


class TestRoutes(unittest.TestCase):
    fake = Fake()

    single_entry_qty = 10

    admin_cred = []
    worker_cred = []
    company_cred = []

    @property
    def admin_profile(self):
        return self.__class__.fake.admin

    @property
    def worker_profile(self):
        return self.__class__.fake.worker

    @property
    def company_profile(self):
        return self.__class__.fake.company

    def get_person_obj(self, kind):
        if kind == 'admin':
            return self.__class__.admin_cred

        elif kind == 'worker':
            return self.__class__.worker_cred

        elif kind == 'company':
            return self.__class__.company_cred


    def new_cred(self, kind, credential):
        person_cred = self.get_person_obj(kind)
        person_cred.append(credential)

    def set_token(self, kind, index, token):
        person_cred = self.get_person_obj(kind)
        person_cred[index]['token'] = token

    def get_token(self, kind, index):
        person_cred = self.get_person_obj(kind)
        return person_cred[index]['token']

    def gen_url(self, resource):
        return '{0}:{1}{2}'.format(
            'http://localhost', config.PORT,
            Formatter.gen_route(resource)
        )

    def write(self, kind):
        person_cred = self.get_person_obj(kind)
        with open(kind + '-credentials.txt', 'w') as f:
            for c in person_cred:
                f.write('{email},{password}\n'.format(**c))

    def test_a_admin_creation(self):
        def gen_admin_profiles():
            for _ in range(0, self.single_entry_qty):
                profile = self.admin_profile

                def get_cred():
                    cred = {}
                    cred['email'] = profile['data']['email']
                    cred['password'] = profile['data']['password']
                    return cred

                self.new_cred('admin', get_cred())

                result = requests.post(
                    self.gen_url('admins'),
                    json=profile
                )

                if not result.status_code == 201:
                    return False

            self.write('admin')
            return True

        self.assertEqual(gen_admin_profiles(), True)

    def test_b_worker_creation(self):
        def gen_worker_profiles():
            for _ in range(0, self.single_entry_qty):
                profile = self.worker_profile

                def get_cred():
                    cred = {}
                    cred['email'] = profile['data']['email']
                    cred['password'] = profile['data']['password']
                    return cred

                self.new_cred('worker', get_cred())

                result = requests.post(
                    self.gen_url('workers'),
                    json=profile
                )

                if not result.status_code == 201:
                    return False

            self.write('worker')
            return True

        self.assertEqual(gen_worker_profiles(), True)

    def test_c_company_creation(self):
        def gen_company_profiles():
            for _ in range(0, self.single_entry_qty):
                profile = self.company_profile

                def get_cred():
                    cred = {}
                    cred['email'] = profile['data']['email']
                    cred['password'] = profile['data']['password']
                    return cred

                self.new_cred('company', get_cred())

                result = requests.post(
                    self.gen_url('companies'),
                    json=profile
                )

                if not result.status_code == 201:
                    return False

            self.write('company')
            return True

        self.assertEqual(gen_company_profiles(), True)

    def test_d_admin_authentication(self):
        def authenticate_admins():
            for i, admin in enumerate(self.__class__.admin_cred):
                result = requests.get(self.gen_url('admins/auth'), json={
                    'email': admin['email'],
                    'password': admin['password']
                })

                if not result.status_code == 200:
                    return False

                response = result.json()
                self.set_token('admin', i, response['data']['token'])

            return True

        self.assertEqual(authenticate_admins(), True)

    def test_e_worker_authentication(self):
        def authenticate_workers():
            for i, worker in enumerate(self.__class__.worker_cred):
                result = requests.get(self.gen_url('workers/auth'), json={
                    'email': worker['email'],
                    'password': worker['password']
                })

                if not result.status_code == 200:
                    return False

                response = result.json()
                self.set_token('worker', i, response['data']['token'])

            return True

        self.assertEqual(authenticate_workers(), True)

    def test_f_company_authentication(self):
        def authenticate_companies():
            for i, company in enumerate(self.__class__.company_cred):
                result = requests.get(self.gen_url('companies/auth'), json={
                    'email': company['email'],
                    'password': company['password']
                })

                if not result.status_code == 200:
                    return False

                response = result.json()
                self.set_token('company', i, response['data']['token'])

            return True

        self.assertEqual(authenticate_companies(), True)

    def test_g_proposal_creation(self):
        def create_proposals():
            for i in range(0, len(self.__class__.company_cred)):
                company_token = self.get_token('company', i)
                company_uid = i + 1
                proposal = self.__class__.fake.proposal(
                    company_uid,
                    company_token,
                    (i % 2 == 0)
                )

                result = requests.post(
                    self.gen_url('proposals'),
                    json=proposal
                )

                if not result.status_code == 201:
                    return False

            return True

        self.assertEqual(create_proposals(), True)

    def test_h_opened_proposals_listing(self):
        pass


if __name__ == '__main__':
    unittest.main()
