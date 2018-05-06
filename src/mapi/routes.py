# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""


from mapi import rapi
from mapi import Formatter

from mapi.resources.address import (AddressInclusion)
from mapi.resources.worker import (WorkerAuthentication)


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

        rapi.add_resource(AddressInclusion, Formatter.gen_route('addresses'))
