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

# Parent directory "injection"
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# Modules
from mapi import db
from mapi.models import (Address,
                         Company,
                         Vehicle,
                         Worker,
                         WorkerAddressAssoc)

# 3rd-party libraries
from faker import Faker
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

        diogo = Worker(name='Diogo Casagrande',
                       telephone='11948211232',
                       email='casagrande.diogo92@gmail.com',
                       rg='098765432',
                       cpf='12345678909',
                       birthday=dio_bday,
                       license_id='0987654321',
                       license_type='B')

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
        self.assertEqual(str(worker), "<Worker 'Caian R. Ertl', '45354686806'>")

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

            vehicle = Vehicle(license=us_fake.numerify(text='#' * 11),
                              model='Modelo ' + us_fake.city_prefix(),
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

        self.assertEqual(len(caian.vehicles), len(diogo.vehicles))

    def test_g_worker_has_addresses(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        worker = Worker.query.get(19)
        home_address = Address.query.get(19)
        work_address = Address.query.get(20)

        worker_has_home_address = WorkerAddressAssoc(worker=worker,
                                                     address=home_address)

        worker_has_work_address = WorkerAddressAssoc(worker=worker,
                                                     address=work_address)

        db.session.add(worker_has_home_address)
        db.session.add(worker_has_work_address)
        db.session.commit()

        worker_addresses = db.session.query(WorkerAddressAssoc).join(Worker).filter(Worker.cpf == '45354686806').all()
        self.assertEqual(len(worker_addresses), 2)

    def test_h_company(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        for i in range(0, 18):
            company = Company(name=us_fake.company(),
                              telephone=us_fake.numerify(text='#' * 10),
                              email=us_fake.company_email(),
                              cnpj=us_fake.numerify(text='#' * 14),
                              opening=us_fake.date_this_century(before_today=True))

            db.session.add(company)

        db.session.commit()

        companies = Company.query.all()
        self.assertEqual(len(companies), 10)

    def test_i_company_has_addresses(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass


if __name__ == '__main__':
    unittest.main()
