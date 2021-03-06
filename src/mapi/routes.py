# -*- coding: utf-8 -*-

# ...
from mapi import rapi
from mapi import Formatter

# ...
from mapi.resources.admin import AdminNew
from mapi.resources.admin import AdminAuth
from mapi.resources.admin import AdminRecord

# ...
from mapi.resources.worker import WorkerNew
from mapi.resources.worker import WorkerAuth
from mapi.resources.worker import WorkerRecord
from mapi.resources.worker import WorkerOffers

# ...
from mapi.resources.company import CompanyNew
from mapi.resources.company import CompanyAuth
from mapi.resources.company import CompanyRecord
from mapi.resources.company import CompanyProposals

# ...
from mapi.resources.proposal import ProposalOffer
from mapi.resources.proposal import ProposalRecord
from mapi.resources.proposal import ProposalResource

# ...
from mapi.resources.ride import RideRecord


class Router:
    @staticmethod
    def include(resource, route):
        rapi.add_resource(resource, Formatter.gen_route(route))

    @staticmethod
    def act():

        # Admins
        Router.include(AdminNew, 'admins')
        Router.include(AdminAuth, 'admins/auth')
        Router.include(AdminRecord, 'admins/<int:uid>')

        # Workers
        Router.include(WorkerNew, 'workers')
        Router.include(WorkerAuth, 'workers/auth')
        Router.include(WorkerRecord, 'workers/<int:uid>')
        Router.include(WorkerOffers, 'workers/<int:uid>/offers')

        # Companies
        Router.include(CompanyNew, 'companies')
        Router.include(CompanyAuth, 'companies/auth')
        Router.include(CompanyRecord, 'companies/<int:uid>')
        Router.include(CompanyProposals, 'companies/<int:uid>/proposals')

        # Proposals
        Router.include(ProposalResource, 'proposals')
        Router.include(ProposalRecord, 'proposals/<int:uid>')
        Router.include(ProposalOffer, 'proposals/<int:uid>/offers')

        # Rides
        Router.include(RideRecord, 'rides')
