#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import unittest
from os import path
from datetime import datetime


sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from mapi import db
from mapi.models import Address


class TestModels(unittest.TestCase):

    def test_address(self):
        address = Address(postcode='07801040', number=255)
        db.session.add(address)
        db.session.commit()

        address_entry = Address.query.get(1)
        self.assertEqual(address_entry.number, 255)


if __name__ == '__main__':
    unittest.main()
