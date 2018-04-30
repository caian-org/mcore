#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import unittest
from os import path
from datetime import datetime


sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from mapi import db
from mapi.models import (Address, Worker)


class TestModels(unittest.TestCase):

    def test_address(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        home_address = Address(postcode='07801040',
                               number='255')

        work_address = Address(postcode='01414003',
                               number='846',
                               complement='Sala 1301')

        db.session.add(home_address)
        db.session.add(work_address)
        db.session.commit()

        address_entries = Address.query.all()
        self.assertEqual(len(address_entries), 2)

    def test_worker(self):
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

        db.session.add(caian)
        db.session.add(diogo)
        db.session.commit()

        worker_entries = Worker.query.all()
        self.assertEqual(len(worker_entries), 2)


if __name__ == '__main__':
    unittest.main()
