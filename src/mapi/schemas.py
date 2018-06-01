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
    """Schema de representação de dados da entidade Admin."""
    class Meta:
        model = Admin


class AddressSchema(Schema):
    """Schema de representação de dados da entidade Address."""
    class Meta:
        model = Address


class CompanySchema(Schema):
    """Schema de representação de dados da entidade Company."""
    class Meta:
        model = Company


class ItemSchema(Schema):
    """Schema de representação de dados da entidade Item."""
    class Meta:
        model = Item


class OfferSchema(Schema):
    """Schema de representação de dados da entidade Offer."""
    class Meta:
        model = Offer


class PersonSchema(Schema):
    """Schema de representação de dados da entidade Person."""
    class Meta:
        model = GenericPerson


class ProposalAddressSchema(Schema):
    class Meta:
        fields = ('complement', 'number', 'postcode')
        model = Address


class ProposalsListSchema(Schema):
    origin = Nested(ProposalAddressSchema)
    destination = Nested(ProposalAddressSchema)

    class Meta:
        fields = ('uid', 'deadline', 'origin', 'destination')
        model = Proposal


class ProposalSchema(Schema):
    """Schema de representação de dados da entidade Proposal."""
    class Meta:
        model = Proposal


class VehicleSchema(Schema):
    """Schema de representação de dados da entidade Vehicle."""
    class Meta:
        model = Vehicle


class WorkerSchema(Schema):
    """Schema de representação de dados da entidade Worker."""
    class Meta:
        fields = ('name', 'email', 'telephone', 'rg', 'cpf', 'license_type',
                  'address_assoc')

        model = Worker
