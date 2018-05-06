# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from mapi import Faker

_fake = Faker()

SECRET_KEY = _fake.password(length=128, special_chars=True, digits=True,
                            upper_case=True, lower_case=True)
