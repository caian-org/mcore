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
        for _ in range(0, 2):
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

    entries = 10

    admin_cred = []
    worker_cred = []
    company_cred = []

    def get_person_credentials(self, kind):
        if kind == 'admin':
            return self.__class__.admin_cred

        elif kind == 'worker':
            return self.__class__.worker_cred

        elif kind == 'company':
            return self.__class__.company_cred

    def set_token(self, kind, index, token):
        person_cred = self.get_person_credentials(kind)
        person_cred[index]['token'] = token

    def get_token(self, kind, index):
        person_cred = self.get_person_credentials(kind)
        return person_cred[index]['token']

    def write(self, kind):
        person_cred = self.get_person_credentials(kind)
        with open(kind + '-credentials.txt', 'w') as f:
            for c in person_cred:
                f.write('{email},{password}\n'.format(**c))

    def gen_url(self, resource):
        return '{0}:{1}{2}'.format(
            'http://localhost', config.PORT,
            Formatter.gen_route(resource)
        )

    def gen_profile(self, kind):
        profile_data = None

        if kind == 'admin':
            profile_data = self.__class__.fake.admin

        elif kind == 'worker':
            profile_data = self.__class__.fake.worker

        elif kind == 'company':
            profile_data = self.__class__.fake.company

        return profile_data

    def create_users(self, route, kind, qty):
        for _ in range(0, qty):
            profile = self.gen_profile(kind)

            person_cred = self.get_person_credentials(kind)
            person_cred.append({
                'email': profile['data']['email'],
                'password': profile['data']['password']
            })

            result = requests.post(
                self.gen_url(route),
                json=profile
            )

            if result.status_code is not 201:
                return False

        person_cred = self.get_person_credentials(kind)
        with open(kind + '-credentials.txt', 'w') as f:
            for c in person_cred:
                f.write('{email},{password}\n'.format(**c))

        return True

    def authenticate_users(self, route, kind):
        person_credentials = self.get_person_credentials(kind)

        for i, person in enumerate(person_credentials):
            result = requests.get(
                self.gen_url(route),
                json={
                    'email': person['email'],
                    'password': person['password']
                })

            if result.status_code is not 200:
                return False

            response = result.json()
            self.set_token(kind, i, response['data']['token'])

        return True

    def test_a_admin_creation(self):
        self.assertTrue(self.create_users('admins', 'admin', self.entries))

    def test_b_worker_creation(self):
        self.assertTrue(self.create_users('workers', 'worker', self.entries))

    def test_c_company_creation(self):
        self.assertTrue(self.create_users('companies', 'company', self.entries))

    def test_d_admin_authentication(self):
        self.assertTrue(self.authenticate_users('admins/auth', 'admin'))

    def test_e_worker_authentication(self):
        self.assertTrue(self.authenticate_users('workers/auth', 'worker'))

    def test_f_company_authentication(self):
        self.assertTrue(self.authenticate_users('companies/auth', 'company'))

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

        self.assertTrue(create_proposals())

    def test_h_list_of_open_proposals(self):
        def assert_both(result):
            code = result.status_code
            content = result.json()['data']

            return code is 200 and len(content) == self.entries / 2

        company_cred = random.choice(self.get_person_credentials('company'))
        result = requests.get(
            self.gen_url('proposals'),
            json={ 'auth': { 'token': company_cred['token'] } }
        )

        self.assertTrue(assert_both(result))

    def test_i_proposal_bidding(self):
        def bid():
            worker_cred = random.choice(self.get_person_credentials('worker'))

            for i in range(0, self.entries):
                id_ = i + 1
                result = requests.post(
                    self.gen_url('proposals/{0}/offer'.format(id_)),
                    json={
                        'auth': { 'token': worker_cred['token'] },
                        'data': { 'workerId': id_,
                                  'price': random.randint(1, 15) * 10000 }
                    })

                if not result.status_code == 201:
                    return False

            return True

        self.assertTrue(bid())


if __name__ == '__main__':
    unittest.main()
