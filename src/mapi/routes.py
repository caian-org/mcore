# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""


from mapi import rapi
from mapi import Formatter

from mapi.resources.address import (AddressRecord, AddressNew)
from mapi.resources.worker import (WorkerRecord, WorkerAuth)


class Router:
    """
    --- TODO: DOCUMENTATION ---
    """

    @staticmethod
    def act():
        """
        --- TODO: DOCUMENTATION ---
        """
        rapi.add_resource(WorkerAuth, Formatter.gen_route('workers/auth'))
        rapi.add_resource(WorkerRecord, Formatter.gen_route('workers/<int:worker_id>'))

        rapi.add_resource(AddressNew, Formatter.gen_route('addresses'))
        rapi.add_resource(AddressRecord, Formatter.gen_route('addresses/<int:address_uid>'))
