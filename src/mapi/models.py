# -*- coding: utf-8 -*-

# Password hashing
from mapi import (gen_phash, check_phash)

# Expirable token generation
from mapi import (Serializer, BadSignature, SignatureExpired)

# Application's configurations
from mapi import config

# Primitive types
from mapi.orm import (Bool, Float, Dat, Int, Str)

# Database objects
from mapi.orm import (Col, Model)

# Relationship objects
from mapi.orm import (BR, FK, Rel)


#        _       _               _   _
#   __ _| |__ __| |_ _ _ __ _ __| |_(_)___ _ _  ___
#  / _` | '_ (_-<  _| '_/ _` / _|  _| / _ \ ' \(_-<
#  \__,_|_.__/__/\__|_| \__,_\__|\__|_\___/_||_/__/
#

class Entity(Model):
    __abstract__ = True

    uid = Col(Int, primary_key=True, autoincrement=True)

    def R(self, attrs):
        class_name = type(self).__name__
        attributes = ', '.join("'{0}'".format(attr) for attr in attrs)

        return '<{0} {1}>'.format(class_name, attributes)

    def __attr__(self):
        pass


class Relation(Model):
    __abstract__ = True


class Person(Entity):
    __abstract__ = True

    name      = Col(Str(64), nullable=False)
    telephone = Col(Str(11), nullable=False)
    email     = Col(Str(64), nullable=False, index=True, unique=True)
    passhash  = Col(Str(128), nullable=False)

    def __attr__(self):
        return self.R([self.name, self.email])

    def set_password(self, password):
        self.passhash = gen_phash(password, salt_length=32)

    def verify_password(self, password):
        return check_phash(self.passhash, password)

    def generate_token(self, expiration=60):
        s = Serializer(config.SECRET_KEY, expires_in=expiration)
        return s.dumps({ 'id': self.uid, 'email': self.email })

    @staticmethod
    def verify_token(token):
        s = Serializer(config.SECRET_KEY)

        try:
            data = s.loads(token)

        except SignatureExpired:
            return False

        except BadSignature:
            return False

        return True


class Human(Person):
    __abstract__ = True

    rg       = Col(Str(9), nullable=False, index=True, unique=True)
    cpf      = Col(Str(11), nullable=False, index=True, unique=True)
    gender   = Col(Str(1), nullable=False, default='M')
    birthday = Col(Dat, nullable=False)


#           _   _ _   _
#   ___ _ _| |_(_) |_(_)___ ___
#  / -_) ' \  _| |  _| / -_|_-<
#  \___|_||_\__|_|\__|_\___/__/
#

class Address(Entity):
    __tablename__ = 'address'

    number     = Col(Str(8))
    complement = Col(Str(16), nullable=True)
    postcode   = Col(Str(8), index=True)

    # Relations
    workers = Rel('Worker', secondary='worker_has_addresses')
    companies = Rel('Company', secondary='company_has_addresses')

    def __repr__(self):
        return self.R([self.postcode, self.number])


class GenericPerson(Person):
    __tablename__ = 'generic_person'


class Admin(Human):
    __tablename__ = 'admininistrator'

    authority_level = Col(Int, nullable=False, index=True)


class Worker(Human):
    __tablename__ = 'worker'

    # Fields
    license_id   = Col(Str(11), nullable=False, index=True, unique=True)
    license_type = Col(Str, nullable=False)

    # Relations
    vehicles = Rel('Vehicle', back_populates='owner')
    offers = Rel('Offer', back_populates='bidder')

    def __repr__(self):
        return self.R([self.name, self.cpf])


class Vehicle(Entity):
    __tablename__ = 'vehicle'

    # Fields
    model = Col(Str(32), nullable=False)
    brand = Col(Str(24), nullable=False)
    plate = Col(Str(8), nullable=False)
    year  = Col(Int, nullable=False)

    # Foreign keys
    owner_uid = Col(Int, FK('worker.uid'))

    # Relations
    owner = Rel(Worker, back_populates='vehicles')

    def __repr__(self):
        return self.R([self.brand, self.year])


class Company(Person):
    __tablename__ = 'company'

    # Fields
    cnpj    = Col(Str(14), nullable=False, index=True, unique=True)
    opening = Col(Dat, nullable=False)

    # Relations
    proposals = Rel('Proposal', back_populates='company')

    def __repr__(self):
        return self.R([self.name, self.cnpj])


class Proposal(Entity):
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
    __tablename__ = 'item'

    fragile = Col(Bool, nullable=False)
    weight  = Col(Float, nullable=False)
    width   = Col(Float, nullable=False)
    height  = Col(Float, nullable=False)

    # Foreign keys
    proposal_uid = Col(Int, FK('proposal.uid'))

    # Relations
    proposal = Rel('Proposal', back_populates='items')


class Offer(Entity):
    __tablename__ = 'offer'

    price = Col(Float, nullable=False)

    # Foreign keys
    bidder_uid = Col(Int, FK('worker.uid'))
    proposal_uid = Col(Int, FK('proposal.uid'))

    # Relations
    bidder = Rel(Worker, back_populates='offers')
    proposal = Rel(Proposal, back_populates='offers')


class Job(Entity):
    __tablename__ = 'job'

    start_date   = Col(Dat, nullable=False)
    end_date     = Col(Dat, nullable=False)
    proposal_uid = Col(Int, FK('proposal.uid'), nullable=False)
    offer_uid    = Col(Int, FK('offer.uid'), nullable=False)
    cost         = Col(Float, nullable=False)


class Invoice(Entity):
    __tablename__ = 'invoice'

    job_uid = Col(Int, FK('job.uid'), nullable=False, unique=True)
    bill    = Col(Float, nullable=False)


#           _      _   _             _    _
#   _ _ ___| |__ _| |_(_)___ _ _  __| |_ (_)_ __ ___
#  | '_/ -_) / _` |  _| / _ \ ' \(_-< ' \| | '_ (_-<
#  |_| \___|_\__,_|\__|_\___/_||_/__/_||_|_| .__/__/
#                                          |_|

class ProposalHasItems(Relation):
    __tablename__ = 'proposal_has_items'

    # Foreign keys
    proposal_uid = Col(Int, FK('proposal.uid'), primary_key=True)
    item_uid     = Col(Int, FK('item.uid'), primary_key=True)

    # Relations
    proposal = Rel(Proposal, backref=BR('item_assoc'))
    item     = Rel(Item, backref=BR('proposal_assoc'))


class WorkerHasAddresses(Relation):
    __tablename__ = 'worker_has_addresses'

    # Foreign keys
    worker_uid = Col(Int, FK('worker.uid'), primary_key=True)
    address_uid = Col(Int, FK('address.uid'), primary_key=True)

    # Relations
    worker  = Rel(Worker, backref=BR('address_assoc'))
    address = Rel(Address, backref=BR('worker_assoc'))


class CompanyHasAddresses(Relation):
    __tablename__ = 'company_has_addresses'

    # Foreign keys
    company_uid = Col(Int, FK('company.uid'), primary_key=True)
    address_uid = Col(Int, FK('address.uid'), primary_key=True)

    # Relations
    company = Rel(Company, backref=BR('address_assoc'))
    address = Rel(Address, backref=BR('company_assoc'))
