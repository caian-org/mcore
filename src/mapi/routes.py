# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""


from mapi import rapi
from mapi import Formatter

from mapi.resources.address import (AddressRecord, AddressNew)
from mapi.resources.worker import (WorkerRecord, WorkerAuth)
from mapi.resources.company import (CompanyRecord)
from mapi.resources.item import (ItemRecord)
from mapi.resources.offer import (OfferRecord)
from mapi.resources.proposal import (ProposalRecord)
from mapi.resources.vehicle import (VehicleProposal)


class Router:
    """
    --- TODO: DOCUMENTATION ---
    """
    @staticmethod
    def include(resource, route):
        """
        --- TODO: DOCUMENTATION ---
        """

        rapi.add_resource(resource, Formatter.gen_route(route))

    @staticmethod
    def act():
        """
        --- TODO: DOCUMENTATION ---
        """

        Router.include(WorkerAuth, 'workers/auth')
        Router.include(WorkerRecord, 'workers/<int:worker_id>')
        Router.include(AddressNew, 'addresses')
        Router.include(AddressRecord, 'addresses/<int:address_id>')
        Router.include(CompanyRecord, 'companies/<int:company_id>')
        Router.include(ItemRecord, 'items/<int:item_id>')
        Router.include(OfferRecord, 'offers/<int:offers_id>')
        Router.include(ProposalRecord, 'proposals/<int:proposal_id>')
        Router.include(VehicleProposal, 'vehicles/<int:vehicle_id>')
