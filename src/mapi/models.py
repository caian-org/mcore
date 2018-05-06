# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

# Primitive types
from mapi.orm import (Bol, Flo, Dat, Int, Str)

# Database objects
from mapi.orm import (Col, Mod)

# Relations
from mapi.orm import (BR, FK, Rel)

# Password hashing
from mapi import (gen_phash, check_phash)

# Expirable token generation
from mapi import (Serializer, BadSignature, SignatureExpired)

# The program's secret keu
from mapi import SECRET_KEY


class Entity(Mod):
    """
    --- TODO: DOCUMENTATION ---
    """
    __abstract__ = True

    uid = Col(Int, primary_key=True, autoincrement=True)

    def R(self, attrs):
        """
        --- TODO: DOCUMENTATION ---
        """
        class_name = type(self).__name__
        attributes = ', '.join("'{0}'".format(attr) for attr in attrs)

        return '<{0} {1}>'.format(class_name, attributes)

    def __attr__(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass


class Relation(Mod):
    """
    --- TODO: DOCUMENTATION ---
    """
    __abstract__ = True


class Person(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __abstract__ = True

    name      = Col(Str(64), nullable=False)
    telephone = Col(Str(11), nullable=False)
    email     = Col(Str(64), nullable=False, index=True, unique=True)
    passhash  = Col(Str(128))

    def __attr__(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        return self.R([self.name, self.email])

    def set_password(self, password):
        """
        --- TODO: DOCUMENTATION ---
        """
        self.passhash = gen_phash(password, salt_length=32)

    def verify_password(self, password):
        """
        --- TODO: DOCUMENTATION ---
        """
        return check_phash(self.passhash, password)

    def generate_token(self, expiration=60):
        """
        --- TODO: DOCUMENTATION ---
        """
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({ 'id': self.uid, 'email': self.email })

    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)

        try:
            data = s.loads(token)

        except SignatureExpired:
            return False

        except BadSignature:
            return False

        return True


class Address(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'address'

    number     = Col(Str(8))
    complement = Col(Str(16), nullable=True)
    postcode   = Col(Str(8), index=True)

    # Relations
    workers = Rel('Worker', secondary='worker_addr_assoc')
    companies = Rel('Company', secondary='company_addr_assoc')

    def __repr__(self):
        return self.R([self.postcode, self.number])


class Worker(Person):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'worker'

    # Fields
    rg           = Col(Str(9), nullable=False, index=True, unique=True)
    cpf          = Col(Str(11), nullable=False, index=True, unique=True)
    birthday     = Col(Dat, nullable=False)
    license_id   = Col(Str(11), nullable=False, index=True, unique=True)
    license_type = Col(Str, nullable=False)

    # Relations
    vehicles = Rel('Vehicle', back_populates='owner')
    offers = Rel('Offer', back_populates='bidder')

    def __repr__(self):
        return self.R([self.name, self.cpf])


class Vehicle(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'vehicle'

    # Fields
    license = Col(Str(11), nullable=False, index=True, unique=True)
    model   = Col(Str(32), nullable=False)
    brand   = Col(Str(24), nullable=False)
    plate   = Col(Str(8), nullable=False)
    year    = Col(Int, nullable=False)

    # Foreign keys
    owner_uid = Col(Int, FK('worker.uid'))

    # Relations
    owner = Rel(Worker, back_populates='vehicles')

    def __repr__(self):
        return self.R([self.brand, self.year])


class Company(Person):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'company'

    # Fields
    cnpj    = Col(Str(14), nullable=False, index=True, unique=True)
    opening = Col(Dat, nullable=False)

    # Relations
    proposals = Rel('Proposal', back_populates='company')

    def __repr__(self):
        return self.R([self.name, self.cnpj])


class Proposal(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'proposal'

    # Fields
    deadline = Col(Dat, nullable=False)

    # Foreign keys
    origin_addr_uid = Col(Int, FK('address.uid'))
    destin_addr_uid = Col(Int, FK('address.uid'))
    company_uid = Col(Int, FK('company.uid'))

    # Relations
    origin = Rel(Address, foreign_keys='Proposal.origin_addr_uid',
                 backref=BR('orig_assoc', uselist=False))

    destination = Rel(Address, foreign_keys='Proposal.destin_addr_uid',
                      backref=BR('dest_assoc', uselist=False))

    company = Rel('Company', back_populates='proposals')
    items   = Rel('Item', back_populates='proposal')
    offers  = Rel('Offer', back_populates='proposal')


class Item(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'item'

    fragile = Col(Bol, nullable=False)
    weight  = Col(Flo, nullable=False)
    width   = Col(Flo, nullable=False)
    height  = Col(Flo, nullable=False)

    # Foreign keys
    proposal_uid = Col(Int, FK('proposal.uid'))

    # Relations
    proposal = Rel('Proposal', back_populates='items')


class Offer(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'offer'

    price = Col(Flo, nullable=False)

    # Foreign keys
    bidder_uid = Col(Int, FK('worker.uid'))
    proposal_uid = Col(Int, FK('proposal.uid'))

    # Relations
    bidder = Rel(Worker, back_populates='offers')
    proposal = Rel(Proposal, back_populates='offers')


class ProposalItemAssoc(Relation):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'proposal_item_assoc'

    # Foreign keys
    proposal_uid = Col(Int, FK('proposal.uid'), primary_key=True)
    item_uid     = Col(Int, FK('item.uid'), primary_key=True)

    # Relations
    proposal = Rel(Proposal, backref=BR('item_assoc'))
    item     = Rel(Item, backref=BR('proposal_assoc'))


class WorkerAddressAssoc(Relation):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'worker_addr_assoc'

    # Foreign keys
    worker_uid = Col(Int, FK('worker.uid'), primary_key=True)
    address_uid = Col(Int, FK('address.uid'), primary_key=True)

    # Relations
    worker  = Rel(Worker, backref=BR('address_assoc'))
    address = Rel(Address, backref=BR('worker_assoc'))


class CompanyAddressAssoc(Relation):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'company_addr_assoc'

    # Foreign keys
    company_uid = Col(Int, FK('company.uid'), primary_key=True)
    address_uid = Col(Int, FK('address.uid'), primary_key=True)

    # Relations
    company = Rel(Company, backref=BR('address_assoc'))
    address = Rel(Address, backref=BR('company_assoc'))
