# -*- coding: utf-8 -*-

from datetime import datetime
from mapi import db


class Entity(db.Model):
    """
    --- TODO: DOCUMENTATION ---
    """
    __abstract__ = True

    uid = db.Column(db.Integer, primary_key=True)


class Person(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __abstract__ = True

    name      = db.Column(db.String(64), nullable=False)
    telephone = db.Column(db.String(11), nullable=False)
    email     = db.Column(db.String(64), nullable=False, index=True, unique=True)
    passhash  = db.Column(db.String())


class Company(Person):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'company'

    cnpj    = db.Column(db.String(14), nullable=False, index=True, unique=True)
    opening = db.Column(db.DateTime, nullable=False)

    # Relations
    compan_addr_relat = db.relationship('compan_addr_relat', backref='addr', lazy='dynamic')
    compan_offe_relat = db.relationship('offer', backref='offer', lazy='dynamic')


class Worker(Person):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'worker'

    license_uid  = db.Column(db.String, nullable=False, index=True, unique=True)
    license_type = db.Column(db.String, nullable=False)
    addr_uid     = db.Column(db.Integer, db.ForeignKey('address.uid'), nullable=False)

    # Relations
    worker_addr_relat = db.relationship('worker_addr_relat', backref='addr', lazy='dynamic')
    worker_offe_relat = db.relationship('offer', backref='addr', lazy='dynamic')
    worker_vehi_relat = db.relationship('vehicle', backref='vehicle', lazy='dynamic')


class Vehicle(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'vehicle'

    license = db.Column(db.String(64), nullable=False, index=True, unique=True)
    model   = db.Column(db.String(24), nullable=False)
    brand   = db.Column(db.String(16), nullable=False)
    year    = db.Column(db.Integer, nullable=False)
    worker_uid = db.Column(db.Integer, db.ForeignKey('worker.uid'), nullable=False)


class Address(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'address'

    number     = db.Column(db.Integer)
    complement = db.Column(db.String(16), nullable=True)
    postcode   = db.Column(db.String(8), index=True)

    # Relations
    addr_worker_relat = db.relationship('worker', backref='address', lazy='dynamic')
    addr_compan_relat = db.relationship('company', backref='address', lazy='dynamic')


class CompanyAddressRelat(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'compan_addr_relat'

    company_uid = db.Column(db.Integer, db.ForeignKey('company.uid'), nullable=False)
    address_uid = db.Column(db.Integer, db.ForeignKey('address.uid'), nullable=False)


class WorkerAddressRelat(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'worker_addr_relat'

    worker_uid  = db.Column(db.Integer, db.ForeignKey('worker.uid'), nullable=False)
    address_uid = db.Column(db.Integer, db.ForeignKey('address.uid'), nullable=False)


class Item(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'item'

    fragile = db.Column(db.Boolean, nullable=False)
    weight  = db.Column(db.Float, nullable=False)
    width   = db.Column(db.Float, nullable=False)
    height  = db.Column(db.Float, nullable=False)

    # Relations
    item_propos_relat = db.relationship('propos_item_relat', backref='prop', lazy='dynamic')


class Proposal(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'proposal'

    origin      = db.Column(db.Integer, db.ForeignKey('address.uid'), nullable=False)
    destination = db.Column(db.Integer, db.ForeignKey('address.uid'), nullable=False)
    company_uid = db.Column(db.Integer, db.ForeignKey('company.uid'), nullable=False)

    # Relations
    propos_offer_relat = db.relationship('offer', backref='offer', lazy='dynamic')
    propos_job_relat   = db.relationship('job', backref='job', lazy='dynamic')
    propos_item_relat  = db.relationship('propos_item_relat', backref='items', lazy='dynamic')


class ProposalItemRelat(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'propos_item_relat'

    proposa_uid = db.Column(db.Integer, db.ForeignKey('proposal.uid'), nullable=False)
    item_uid    = db.Column(db.Integer, db.ForeignKey('item.uid'), nullable=False)


class Offer(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'offer'

    proposa_uid = db.Column(db.Integer, db.ForeignKey('proposal.uid'), nullable=False)
    worker_uid  = db.Column(db.Integer, db.ForeignKey('worker.uid'), nullable=False)
    price       = db.Column(db.Float, nullable=False)

    # Relations
    offer_job_relat = db.relationship('job', backref='job', lazy='dynamic')


class Job(Entity):
    """
    --- TODO: DOCUMENTATION ---
    """
    __tablename__ = 'job'

    proposa_uid = db.Column(db.Integer, db.ForeignKey('proposal.uid'), nullable=False)
    offer_uid   = db.Column(db.Integer, db.ForeignKey('offer.uid'), nullable=False)
    status      = db.Column(db.Integer, nullable=False)
