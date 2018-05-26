# -*- coding: utf-8 -*-

# ...
from datetime import datetime

# Database connection
from . import db

# Worker model
from . import Company
from . import Address
from . import CompanyHasAddresses

# Worker datatype schema
from . import CompanySchema

# HTTP-related
from . import Resource
from . import request
from . import response

# Authentication logic
from .person import PersonNew
from .person import PersonAuth
from .person import PersonRecord

# Form/JSON data authenticator
from .auth import Authenticator


class CompanyAuth(PersonAuth):
    entity = Company


class CompanyNew(PersonNew):
    entity = Company
    schema = CompanySchema

    def post(self):
        payload = request.get_json()

        if not Authenticator.check_struct(payload, ['data']):
            return response.bad_request

        data = payload['data']
        required = ['address']
        if not Authenticator.check_struct(data, required):
            return response.bad_request

        address = data['address']

        params = [
            data.get('name'),
            data.get('email'),
            data.get('cnpj'),
            data.get('opening'),
            data.get('telephone'),
            data.get('password'),
            address.get('number'),
            address.get('postcode')
        ]

        if not Authenticator.check_payload(params):
            return response.bad_request

        data['opening'] = datetime.strptime(data['opening'], '%d-%m-%Y')

        company = self.new(name=data['name'],
                           email=data['email'],
                           cnpj=data['cnpj'],
                           opening=data['opening'],
                           telephone=data['telephone'])

        company.set_password(data['password'])

        address = Address(postcode=address['postcode'],
                          number=address['number'],
                          complement=address['complement'])

        db.session.add(company)
        db.session.add(address)
        db.session.commit()

        company_address = CompanyHasAddresses(company=company, address=address)

        db.session.add(company_address)
        db.session.commit()

        return response.created('companies', company.uid)


class CompanyRecord(PersonRecord):
    entity = Company
    schema = CompanySchema

    def delete(self):
        pass

    def put(self):
        pass


class CompanyProposals(Resource):
    pass
