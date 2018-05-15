# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""


from mapi import (rapi, Formatter)

from mapi.resources.worker   import *
from mapi.resources.company  import *
from mapi.resources.offer    import *
from mapi.resources.proposal import *


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
        Router.include(WorkerRecord, 'workers/<int:uid>')
        Router.include(WorkerAddresses, 'workers/<int:uid>/addresses')
        Router.include(WorkerVehicles, 'workers/<int:uid>/vehicles')

        # Companies
        Router.include(CompanyNew, 'companies')
        Router.include(CompanyAuth, 'companies/auth')
        Router.include(CompanyRecord, 'companies/<int:uid>')
        Router.include(CompanyProposals, 'companies/<int:uid>/proposals')

        # Offers
        Router.include(OfferNew, 'offers')
        Router.include(OfferRecord, 'offers/<int:uid>')

        # Proposals
        Router.include(ProposalNew, 'proposals')
        Router.include(ProposalRecord, 'proposals/<int:uid>')
