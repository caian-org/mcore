# -*- coding: utf-8 -*-

# ...
from mapi import rapi
from mapi import Formatter

# ...
from mapi.resources.admin import AdminNew
from mapi.resources.admin import AdminAuth
from mapi.resources.worker import WorkerNew
from mapi.resources.worker import WorkerAuth
from mapi.resources.worker import WorkerRecord
from mapi.resources.company import CompanyNew
from mapi.resources.company import CompanyAuth
from mapi.resources.company import CompanyRecord
from mapi.resources.proposal import ProposalOffer
from mapi.resources.proposal import ProposalRecord
from mapi.resources.proposal import ProposalResource


class Router:
    @staticmethod
    def include(resource, route):
        rapi.add_resource(resource, Formatter.gen_route(route))

    @staticmethod
    def act():

        # Admins
        Router.include(AdminNew, 'admins')
        Router.include(AdminAuth, 'admins/auth')

        # Workers
        Router.include(WorkerNew, 'workers')
        Router.include(WorkerAuth, 'workers/auth')
        Router.include(WorkerRecord, 'workers/<int:uid>')

        # Companies
        Router.include(CompanyNew, 'companies')
        Router.include(CompanyAuth, 'companies/auth')
        Router.include(CompanyRecord, 'companies/<int:uid>')

        # Proposals
        Router.include(ProposalResource, 'proposals')
        Router.include(ProposalRecord, 'proposals/<int:uid>')
        Router.include(ProposalOffer, 'proposals/<int:uid>/offer')
