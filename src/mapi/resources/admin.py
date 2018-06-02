# -*- coding: utf-8 -*-

# ...
from datetime import datetime

# Database connection
from . import db

# Admin model and related ones
from . import Admin
from . import Address
from . import AdminHasAddresses

# Admin datatype schema
from . import AdminSchema

# HTTP-related
from . import Resource
from . import request
from . import response

# Authentication logic
from .person import PersonNew
from .person import PersonAuth
from .person import PersonRecord

# Form/JSON data validator
from .auth import Validator


class AdminAuth(PersonAuth):
    entity = Admin


class AdminNew(PersonNew):
    entity = Admin
    schema = AdminSchema

    def post(self):
        payload = request.get_json()

        if not Validator.check_struct(payload, ['data']):
            return response.bad_request

        data = payload['data']
        required = ['address']
        if not Validator.check_struct(data, required):
            return response.bad_request

        address = data['address']

        params = [
            data.get('name'),
            data.get('telephone'),
            data.get('email'),
            data.get('password'),
            data.get('rg'),
            data.get('cpf'),
            data.get('gender'),
            data.get('birthday'),
            data.get('authorityLevel'),
            address.get('number'),
            address.get('postcode')
        ]

        if not Validator.check_payload(params):
            return response.bad_request

        data['birthday'] = datetime.strptime(data['birthday'], '%d-%m-%Y')

        admin = self.new(name=data['name'],
                         telephone=data['telephone'],
                         email=data['email'],
                         rg=data['rg'],
                         cpf=data['cpf'],
                         gender=data['gender'],
                         birthday=data['birthday'],
                         authority_level=data['authorityLevel'])

        admin.set_password(data['password'])

        address = Address(postcode=address['postcode'],
                          number=address['number'],
                          complement=address['complement'])

        db.session.add(admin)
        db.session.add(address)
        db.session.commit()

        admin_address = AdminHasAddresses(admin=admin, address=address)

        db.session.add(admin_address)
        db.session.commit()

        return response.created('admins', admin.uid)

class AdminRecord(PersonRecord):
    entity = Admin
    schema = AdminSchema
