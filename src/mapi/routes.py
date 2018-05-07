# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""


from mapi import (rapi, Formatter)

from mapi.resources.worker   import (WorkerRecord, WorkerNew, WorkerAuth)
from mapi.resources.company  import (CompanyRecord, CompanyNew)

from mapi.resources.address  import (AddressRecord, AddressNew)
from mapi.resources.item     import (ItemRecord, ItemNew)
from mapi.resources.offer    import (OfferRecord, OfferNew)
from mapi.resources.proposal import (ProposalRecord, ProposalNew)
from mapi.resources.vehicle  import (VehicleRecord, VehicleNew)


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

        # Workers
        Router.include(WorkerNew, 'workers')
        Router.include(WorkerAuth, 'workers/auth')
        Router.include(WorkerRecord, 'workers/<int:worker_id>')

        # Addresses
        Router.include(AddressNew, 'addresses')
        Router.include(AddressRecord, 'addresses/<int:address_id>')

        # Companies
        Router.include(CompanyNew, 'companies')
        Router.include(CompanyRecord, 'companies/<int:company_id>')

        # Items
        Router.include(ItemNew, 'items')
        Router.include(ItemRecord, 'items/<int:item_id>')

        # Offers
        Router.include(OfferNew, 'offers')
        Router.include(OfferRecord, 'offers/<int:offers_id>')

        # Proposals
        Router.include(ProposalNew, 'proposals')
        Router.include(ProposalRecord, 'proposals/<int:proposal_id>')

        # Vehicles
        Router.include(VehicleNew, 'vehicles')
        Router.include(VehicleRecord, 'vehicles/<int:vehicle_id>')
