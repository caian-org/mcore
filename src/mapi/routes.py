# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""


from mapi import rapi
from mapi import Formatter

from mapi.resources.address import (Address, AddressInclusion)
from mapi.resources.worker import (Worker, WorkerAuthentication)


class Router:
    """
    --- TODO: DOCUMENTATION ---
    """

    @staticmethod
    def act():
        """
        --- TODO: DOCUMENTATION ---
        """
        rapi.add_resource(WorkerAuthentication, Formatter.gen_route('workers/auth'))
        rapi.add_resource(Worker, Formatter.gen_route('workers/<int:worker_id>'))

        rapi.add_resource(AddressInclusion, Formatter.gen_route('addresses'))
        rapi.add_resource(Address, Formatter.gen_route('addresses/<int:address_uid>'))
