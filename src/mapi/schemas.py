# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from mapi.orm import Schema
from mapi.models import Worker


class WorkerSchema(Schema):
    """
    --- TODO: DOCUMENTATION ---
    """
    class Meta:
        fields = ('name', 'email', 'telephone', 'rg', 'cpf', 'license_type',
                  'address_assoc')

        model = Worker
