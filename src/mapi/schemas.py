# -*- coding: utf-8 -*-

from mapi.orm import Schema
from mapi.orm import Nested

from mapi.models import Admin
from mapi.models import Address
from mapi.models import Company
from mapi.models import Item
from mapi.models import Offer
from mapi.models import GenericPerson
from mapi.models import Proposal
from mapi.models import Vehicle
from mapi.models import Worker


class AdminSchema(Schema):
    '''Schema de representação de dados da entidade Admin.'''
    class Meta:
        model = Admin


class AddressSchema(Schema):
    '''Schema de representação de dados da entidade Address.'''
    class Meta:
        model = Address


class CompanySchema(Schema):
    '''Schema de representação de dados da entidade Company.'''
    class Meta:
        fields = (
            'name', 'email', 'telephone', 'cnpj', 'opening'
        )
        model = Company


class ItemSchema(Schema):
    '''Schema de representação de dados da entidade Item.'''
    class Meta:
        fields = (
            'title', 'width', 'weight', 'height', 'fragile'
        )
        model = Item


class PersonSchema(Schema):
    '''Schema de representação de dados da entidade Person.'''
    class Meta:
        model = GenericPerson


class VehicleSchema(Schema):
    '''Schema de representação de dados da entidade Vehicle.'''
    class Meta:
        fields = (
            'brand', 'model', 'plate', 'year'
        )
        model = Vehicle


class WorkerSchema(Schema):
    '''Schema de representação de dados da entidade Worker.'''
    vehicles = Nested(VehicleSchema, many=True)

    class Meta:
        fields = (
            'name', 'email', 'telephone', 'rg', 'cpf', 'gender',
            'birthday', 'license_id', 'license_type', 'vehicles'
        )
        model = Worker


class BidderSchema(Schema):
    '''Schema de representação do motorista que realizou o lance de proposta.'''
    class Meta:
        fields = (
            'uid', 'name'
        )
        model = Worker


class OfferSchema(Schema):
    '''Schema de representação de um lance em uma proposta.'''
    bidder = Nested(BidderSchema)

    class Meta:
        fields = (
            'uid', 'price', 'bidder'
        )
        model = Offer


#                                   _
#   _ __ _ _ ___ _ __  ___ ___ __ _| |___
#  | '_ \ '_/ _ \ '_ \/ _ (_-</ _` | (_-<
#  | .__/_| \___/ .__/\___/__/\__,_|_/__/
#  |_|          |_|
class ProposalAddressSchema(Schema):
    '''Schema de representação dos endereços de uma proposta.'''
    class Meta:
        fields = (
            'complement', 'number', 'postcode'
        )
        model = Address


class ProposalCompanySchema(Schema):
    '''Schema de representação da empresa emissora da proposta.'''
    class Meta:
        fields = (
            'uid', 'name'
        )
        model = Company


class ProposalSchema(Schema):
    '''Schema de representação de uma única proposta.'''
    items = Nested(ItemSchema, many=True)
    offers = Nested(OfferSchema, many=True)
    origin = Nested(ProposalAddressSchema)
    company = Nested(ProposalCompanySchema)
    destination = Nested(ProposalAddressSchema)

    class Meta:
        fields = (
            'uid', 'title', 'status', 'deadline', 'description',
            'items', 'offers', 'origin', 'company', 'destination'
        )
        model = Proposal


class ProposalsListSchema(Schema):
    '''Schema de representação da lista de propostas abertas.'''
    company = Nested(ProposalCompanySchema)

    class Meta:
        fields = (
            'uid', 'title', 'deadline', 'company'
        )
        model = Proposal
