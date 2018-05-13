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


class TestModels(unittest.TestCase):
    """
    --- TODO: DOCUMENTATION ---
    """

    def test_a_address(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        worker_home_address = Address(postcode='07801040',
                                      number='255')

        worker_work_address = Address(postcode='01414003',
                                      number='846',
                                      complement='Sala 1301')

        for i in range(0, 18):
            company_address = Address(postcode=br_fake.postcode().replace('-', ''),
                                      number=br_fake.building_number(),
                                      complement='Sala ' + br_fake.random_uppercase_letter())

            db.session.add(company_address)

        db.session.add(worker_home_address)
        db.session.add(worker_work_address)

        db.session.commit()

        address_entries = Address.query.all()
        self.assertEqual(len(address_entries), 20)

    def test_b_single_address(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        home_address = Address.query.get(19)
        self.assertEqual(home_address.postcode, '07801040')

    def test_c_worker(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        cai_bday = datetime(1997, 2, 25)
        dio_bday = datetime(1995, 1, 1)

        caian = Worker(name='Caian R. Ertl',
                       telephone='11981615593',
                       email='caianrais@gmail.com',
                       rg='429075406',
                       cpf='45354686806',
                       birthday=cai_bday,
                       license_id='1234567890',
                       license_type='A')

        caian.set_password('rechtsschutzversicherungsgesellschaften')

        diogo = Worker(name='Diogo Casagrande',
                       telephone='11948211232',
                       email='casagrande.diogo92@gmail.com',
                       rg='098765432',
                       cpf='12345678909',
                       birthday=dio_bday,
                       license_id='0987654321',
                       license_type='B')

        diogo.set_password('supercalifragilisticexpialidocious')

        for i in range(0, 18):
            tel = br_fake.phone_number()\
                .replace('(', '')\
                .replace(')', '')\
                .replace(' ', '')\
                .replace('-', '')\
                .replace('+55', '')

            worker = Worker(name=br_fake.name(),
                            telephone=tel,
                            email=br_fake.email(),
                            rg=br_fake.numerify(text='#' * 9),
                            cpf=br_fake.numerify(text='#' * 11),
                            birthday=br_fake.date_this_century(before_today=True),
                            license_id=br_fake.numerify(text='#' * 11),
                            license_type=br_fake.random_uppercase_letter())

            worker.set_password(us_fake.password(length=32, special_chars=True,
                                                 digits=True, upper_case=True,
                                                 lower_case=True))

            db.session.add(worker)

        db.session.add(caian)
        db.session.add(diogo)
        db.session.commit()

        worker_entries = Worker.query.all()
        self.assertEqual(len(worker_entries), 20)

    def test_d_worker_repr(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        worker = Worker.query.get(19)
        repr_ = "<Worker 'Caian R. Ertl', '45354686806'>"
        self.assertEqual(str(worker), repr_)

    def test_e_vehicle(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        caian = Worker.query.get(19)
        diogo = Worker.query.get(20)

        for i in range(0, 10):
            owner = diogo
            if i % 2 == 0:
                owner = caian

            vehicle = Vehicle(model='Modelo ' + us_fake.city_prefix(),
                              brand=us_fake.company(),
                              plate=br_fake.license_plate(),
                              year=br_fake.year(),
                              owner=owner)

            db.session.add(vehicle)

        db.session.commit()

        vehicles = Vehicle.query.all()
        self.assertEqual(len(vehicles), 10)

    def test_f_worker_has_vehicles(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        caian = Worker.query.get(19)
        diogo = Worker.query.get(20)

        def assertion(a=caian.vehicles, b=diogo.vehicles):
            return len(a) == 5 and len(b) == 5

        self.assertEqual(assertion(), True)

    def test_g_worker_has_addresses(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        worker = Worker.query.get(19)
        home_address = Address.query.get(19)
        work_address = Address.query.get(20)

        worker_has_home_address = WorkerHasAddresses(worker=worker,
                                                     address=home_address)

        worker_has_work_address = WorkerHasAddresses(worker=worker,
                                                     address=work_address)

        db.session.add(worker_has_home_address)
        db.session.add(worker_has_work_address)
        db.session.commit()

        worker_addresses = db.session.query(WorkerHasAddresses)\
            .join(Worker)\
            .filter(Worker.cpf == '45354686806')\
            .all()

        self.assertEqual(len(worker_addresses), 2)

    def test_h_company(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        evil_corp = Company(name='E Corp',
                            telephone='2128046003',
                            email='contact@ecorp.com',
                            cnpj='12345678909876',
                            opening=datetime(1985, 7, 1))

        evil_corp.set_password('Phillip_Price1995')

        acme_corp = Company(name='Acme Corporation',
                            telephone='6662018666',
                            email='sales@acme.com',
                            cnpj='98765432123456',
                            opening=datetime(1870, 1, 1))

        acme_corp.set_password('Wile.E.Coyote')

        for i in range(0, 18):
            company = Company(name=us_fake.company(),
                              telephone=us_fake.numerify(text='#' * 10),
                              email=us_fake.company_email(),
                              cnpj=us_fake.numerify(text='#' * 14),
                              opening=us_fake.date_this_century(before_today=True))

            company.set_password(us_fake.password(length=32, special_chars=True,
                                                  digits=True, upper_case=True,
                                                  lower_case=True))

            db.session.add(company)

        db.session.add(evil_corp)
        db.session.add(acme_corp)

        db.session.commit()

        companies = Company.query.all()
        self.assertEqual(len(companies), 20)

    def test_i_company_has_addresses(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        evil_corp = Company.query.get(19)
        acme_corp = Company.query.get(20)

        assoc_entries = []
        for i in range(0, 18):
            addr = Address.query.get((i + 1))

            company_address = None
            if i % 2 == 0:
                company_address = CompanyHasAddresses(company=acme_corp, address=addr)
            else:
                company_address = CompanyHasAddresses(company=evil_corp, address=addr)

            assoc_entries.append(company_address)

        for company_address_assoc in assoc_entries:
            db.session.add(company_address_assoc)

        db.session.commit()

        evil_corp_addresses = db.session.query(CompanyHasAddresses)\
            .join(Company)\
            .filter(Company.cnpj == '12345678909876')\
            .all()

        acme_corp_addresses = db.session.query(CompanyHasAddresses)\
            .join(Company)\
            .filter(Company.cnpj == '98765432123456')\
            .all()

        def assertion(a=evil_corp_addresses, b=acme_corp_addresses):
            return len(a) == 9 and len(b) == 9

        self.assertEqual(assertion(), True)

    def test_j_proposal(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        origin_address = Address.query.get(10)
        destination_address = Address.query.get(11)

        evil_corp = Company.query.get(1)

        proposal = Proposal(deadline=datetime(2018, 12, 25),
                            origin=origin_address,
                            destination=destination_address,
                            company=evil_corp)

        db.session.add(proposal)
        db.session.commit()

        proposals = Proposal.query.all()
        self.assertEqual(len(proposals), 1)

    def test_k_item(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        proposal = Proposal.query.get(1)

        item = Item(fragile=False,
                    weight=5.0,
                    width=0.8,
                    height=0.5,
                    proposal=proposal)

        db.session.add(item)
        db.session.commit()

        items = Item.query.all()
        self.assertEqual(len(items), 1)

    def test_l_offer(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        caian = Worker.query.get(19)
        proposal = Proposal.query.get(1)

        offer = Offer(price=1000,
                      bidder=caian,
                      proposal=proposal)

        db.session.add(offer)
        db.session.commit()

        offers = Offer.query.all()
        self.assertEqual(len(offers), 1)


class TestRoutes(unittest.TestCase):
    """
    --- TODO: DOCUMENTATION ---
    """
    worker_token = None

    def gen_url(self, resource):
        """
        --- TODO: DOCUMENTATION ---
        """
        return '{0}:{1}{2}'.format(
            'http://localhost', config.PORT,
            Formatter.gen_route(resource)
        )

    def test_a_worker_authentication(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        result = requests.post(self.gen_url('workers/auth'), json={
            'email': 'caianrais@gmail.com',
            'password': 'rechtsschutzversicherungsgesellschaften'
        })

        if not result.status_code == 200:
            self.fail('Request failed. Code: ' + result.status_code)

        response = result.json()
        self.__class__.worker_token = response['data']['token']

        self.assertIsNotNone(self.worker_token)

    def test_b_address_creation_by_worker(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        result = requests.post(self.gen_url('addresses'), json={
            'auth': {
                'token': self.__class__.worker_token
            },

            'data': {
                'postcode': '07801040',
                'number': '255',
                'complement': 'home'
            }
        })

        self.assertEqual(result.status_code, 201)

    def test_c_get_worker_information(self):
        result = requests.get(self.gen_url('workers/19'), json={
            'auth': {
                'token': self.__class__.worker_token
            }
        })

        self.assertEqual(result.status_code, 200)

    def test_d_company_authentication(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        result = requests.post(self.gen_url('companies/auth'), json={
            'email': 'contact@ecorp.com',
            'password': 'Phillip_Price1995'
        })

        if not result.status_code == 200:
            self.fail('Request failed. Code: ' + result.status_code)

        response = result.json()
        self.__class__.company_token = response['data']['token']

        self.assertIsNotNone(self.company_token)

    def test_e_get_company_information(self):
        result = requests.get(self.gen_url('companies/19'), json={
            'auth': {
                'token': self.__class__.company_token
            }
        })

        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()
