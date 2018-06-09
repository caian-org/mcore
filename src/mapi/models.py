# -*- coding: utf-8 -*-

# Hashing de senhas
from mapi import gen_phash
from mapi import check_phash

# Geração de tokens expiráveis
from mapi import Serializer
from mapi import BadSignature
from mapi import SignatureExpired

# Configurações da aplicação
from mapi import config

# Tipos primitivos de dados
from mapi.orm import Dat
from mapi.orm import Int
from mapi.orm import Str
from mapi.orm import Bool
from mapi.orm import Float

# Objetos do banco de dados (modelos e colunas)
from mapi.orm import Col
from mapi.orm import Model

# Relacionamentos do ORM
from mapi.orm import BR
from mapi.orm import FK
from mapi.orm import Rel


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

    name = Col(Str(64), nullable=False)
    email = Col(Str(64), nullable=False, index=True, unique=True)
    passhash = Col(Str(128), nullable=False)
    telephone = Col(Str(11), nullable=False)

    def __attr__(self):
        return self.R([self.name, self.email])

    def set_password(self, password):
        self.passhash = gen_phash(password, salt_length=32)

    def verify_password(self, password):
        return check_phash(self.passhash, password)

    def generate_token(self, expiration=60):
        s = Serializer(config.SECRET_KEY, expires_in=expiration)
        return s.dumps({ 'id': self.uid, 'kind': self.__tablename__ })

    @staticmethod
    def verify_token(token):
        s = Serializer(config.SECRET_KEY)

        try:
            data = s.loads(token)

        except (SignatureExpired, BadSignature):
            data = None

        finally:
            return data


class Human(Person):
    __abstract__ = True

    rg = Col(Str(9), nullable=False, index=True, unique=True)
    cpf = Col(Str(11), nullable=False, index=True, unique=True)
    gender = Col(Str(1), nullable=False, default='M')
    birthday = Col(Dat, nullable=False)


#           _   _ _   _
#   ___ _ _| |_(_) |_(_)___ ___
#  / -_) ' \  _| |  _| / -_|_-<
#  \___|_||_\__|_|\__|_\___/__/
#
class Address(Entity):
    __tablename__ = 'address'

    number = Col(Str(8))
    postcode = Col(Str(8), index=True)
    complement = Col(Str(16), nullable=True)

    # Relations
    admins = Rel('Admin', secondary='admin_has_addresses')
    workers = Rel('Worker', secondary='worker_has_addresses')
    companies = Rel('Company', secondary='company_has_addresses')

    def __repr__(self):
        return self.R([self.postcode, self.number])


class GenericPerson(Person):
    __tablename__ = 'generic_person'


class Admin(Human):
    __tablename__ = 'administrator'

    # Fields
    authority_level = Col(Int, nullable=False, index=True)


class Worker(Human):
    __tablename__ = 'worker'

    # Fields
    license_id = Col(Str(11), nullable=False, index=True, unique=True)
    license_type = Col(Str, nullable=False)

    # Relations
    vehicles = Rel('Vehicle', back_populates='owner')
    offers = Rel('Offer', back_populates='bidder')

    def __repr__(self):
        return self.R([self.name, self.cpf])


class Vehicle(Entity):
    __tablename__ = 'vehicle'

    # Fields
    year = Col(Int, nullable=False)
    model = Col(Str(32), nullable=False)
    brand = Col(Str(24), nullable=False)
    plate = Col(Str(8), nullable=False)

    # Foreign keys
    owner_uid = Col(Int, FK('worker.uid'))

    # Relations
    owner = Rel(Worker, back_populates='vehicles')

    def __repr__(self):
        return self.R([self.brand, self.year])


class Company(Person):
    __tablename__ = 'company'

    # Fields
    cnpj = Col(Str(14), nullable=False, index=True, unique=True)
    opening = Col(Dat, nullable=False)

    # Relations
    proposals = Rel('Proposal', back_populates='company')

    def __repr__(self):
        return self.R([self.name, self.cnpj])


class Proposal(Entity):
    __tablename__ = 'proposal'

    # Fields
    title = Col(Str, nullable=False)
    status = Col(Bool, nullable=False)
    deadline = Col(Dat, nullable=False)
    description = Col(Str, nullable=True)

    # Foreign keys
    company_uid = Col(Int, FK('company.uid'))
    origin_addr_uid = Col(Int, FK('address.uid'))
    destin_addr_uid = Col(Int, FK('address.uid'))

    # Relations
    origin = Rel(Address, foreign_keys='Proposal.origin_addr_uid',
                 backref=BR('orig_assoc', uselist=False))

    destination = Rel(Address, foreign_keys='Proposal.destin_addr_uid',
                      backref=BR('dest_assoc', uselist=False))

    items = Rel('Item', back_populates='proposal')
    offers = Rel('Offer', back_populates='proposal')
    company = Rel('Company', back_populates='proposals')


class Item(Entity):
    __tablename__ = 'item'

    title = Col(Str, nullable=False)
    width = Col(Float, nullable=False)
    weight = Col(Float, nullable=False)
    height = Col(Float, nullable=False)
    fragile = Col(Bool, nullable=False)

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

    cost = Col(Float, nullable=False)
    end_date = Col(Dat, nullable=False)
    offer_uid = Col(Int, FK('offer.uid'), nullable=False)
    start_date = Col(Dat, nullable=False)
    proposal_uid = Col(Int, FK('proposal.uid'), nullable=False)


class Invoice(Entity):
    __tablename__ = 'invoice'

    bill = Col(Float, nullable=False)
    job_uid = Col(Int, FK('job.uid'), nullable=False, unique=True)


#           _      _   _             _    _
#   _ _ ___| |__ _| |_(_)___ _ _  __| |_ (_)_ __ ___
#  | '_/ -_) / _` |  _| / _ \ ' \(_-< ' \| | '_ (_-<
#  |_| \___|_\__,_|\__|_\___/_||_/__/_||_|_| .__/__/
#                                          |_|
class WorkerHasAddresses(Relation):
    __tablename__ = 'worker_has_addresses'

    # Foreign keys
    worker_uid = Col(Int, FK('worker.uid'), primary_key=True)
    address_uid = Col(Int, FK('address.uid'), primary_key=True)

    # Relations
    worker = Rel(Worker, backref=BR('address_assoc'))
    address = Rel(Address, backref=BR('worker_assoc'))


class CompanyHasAddresses(Relation):
    __tablename__ = 'company_has_addresses'

    # Foreign keys
    company_uid = Col(Int, FK('company.uid'), primary_key=True)
    address_uid = Col(Int, FK('address.uid'), primary_key=True)

    # Relations
    company = Rel(Company, backref=BR('address_assoc'))
    address = Rel(Address, backref=BR('company_assoc'))


class AdminHasAddresses(Relation):
    __tablename__ = 'admin_has_addresses'

    # Foreign keys
    admin_uid = Col(Int, FK('administrator.uid'), primary_key=True)
    address_uid = Col(Int, FK('address.uid'), primary_key=True)

    # Relations
    admin = Rel(Admin, backref=BR('address_assoc'))
    address = Rel(Address, backref=BR('admin_assoc'))
