# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from mapi.orm import Schema
from mapi.models import (Address, Company, Entity, Item,
                         Offer, Proposal, Vehicle, Worker)


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
