# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

# Database connection
from . import db

# Worker model and related ones
from . import (Worker, Address, WorkerHasAddresses, Vehicle)

# Worker datatype schema
from . import WorkerSchema

# HTTP-related
from . import (Resource, request, response)

# Authentication logic
from .person import (PersonAuth, PersonRecord, PersonNew)

# Form/JSON data authenticator
from .auth import Authenticator


class WorkerAuth(PersonAuth):
    """
    --- TODO: DOCUMENTATION ---
    """

    entity = Worker


class WorkerNew(PersonNew):
    """
    --- TODO: DOCUMENTATION ---
    """

    entity = Worker
    schema = WorkerSchema

    def post(self):
        payload = request.get_json()
        success, result = WorkerAuth.authenticate(payload)

        if not success:
            return result

        if not Authenticator.check_struct(payload, ['data']):
            return response.bad_request

        data = payload['data']
        required = ['address', 'vehicle']
        if not Authenticator.check_struct(data, required):
            return response.bad_request

        address = data['address']
        vehicle = data['vehicle']

        params = [
            data.get('name'),
            data.get('telephone'),
            data.get('email'),
            data.get('password'),
            data.get('rg'),
            data.get('cpf'),
            data.get('gender'),
            data.get('birthday'),
            data.get('licenceId'),
            data.get('licenseType'),
            vehicle.get('model'),
            vehicle.get('brand'),
            vehicle.get('plate'),
            vehicle.get('year'),
            address.get('number'),
            address.get('postcode')
        ]

        if not Authenticator.check_payload(params):
            return response.bad_request

        worker = self.new(name=data['name'],
                          telephone=data['tel'],
                          email=data['email'],
                          rg=data['rg'],
                          cpf=data['cpf'],
                          birthday=data['bday'],
                          license_id=data['lic_id'],
                          license_type=data['lic_ty'])

        address = Address(postcode=address['postcode'],
                          number=address['number'],
                          complement=address['complement'])

        db.session.add(worker)
        db.session.add(address)
        db.session.commit()

        vehicle = Vehicle(model=vehicle['model'],
                          brand=vehicle['brand'],
                          plate=vehicle['plate'],
                          year=vehicle['year'],
                          owner=worker)

        worker_address = WorkerHasAddresses(worker=worker, address=address)

        db.session.add(vehicle)
        db.session.add(worker_address)
        db.session.commit()

        return response.SUCCESS(201, 'ok')


class WorkerRecord(PersonRecord):
    """
    --- TODO: DOCUMENTATION ---
    """
    entity = Worker
    schema = WorkerSchema


class WorkerAddresses(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """
    pass


class WorkerVehicles(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """
    pass
