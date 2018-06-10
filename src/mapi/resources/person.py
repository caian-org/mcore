# -*- coding: utf-8 -*-

# ...
from . import db

# ...
from . import Person

# ...
from . import PersonSchema
from . import AddressSchema

# ...
from . import Resource
from . import request
from . import response

# ...
from .auth import Validator
from .auth import Authorizer


class PersonAuth(Resource):
    entity = Person

    @staticmethod
    def authenticate(payload):
        """
        Método de autenticação de token
        """
        if not Validator.check_struct(payload, ['auth']):
            return False, response.bad_request

        auth = payload['auth']
        token = auth.get('token')

        if not token:
            return False, response.bad_request

        if not Validator.verify_token(token):
            return False, response.forbidden

        return True, None

    def get(self):
        """
        Método de autenticação do usuário via email e senha (aka login)
        """
        payload = request.get_json()
        email = payload.get('email')
        passw = payload.get('password')

        if not email or not passw:
            return response.bad_request

        person = self.entity.query.filter_by(email=email).all()
        if not person:
            return response.incorrect_email_or_password

        person = person[0]
        valid_passw = person.verify_password(passw)
        if not valid_passw:
            return response.incorrect_email_or_password

        token = person.generate_token()
        return response.ok({
            'token': token.decode('ascii')
        })


class PersonNew(Resource):
    entity = Person
    schema = PersonSchema

    def new(self, **kwargs):
        return self.entity(**kwargs)


class PersonRecord(Resource):
    access_kind = 'any'
    entity = Person
    schema = PersonSchema
    addresses = None

    def delete(self):
        pass

    def get(self, uid):
        # Verifica a estrutura da requisição, se o usuário está autenticado e é
        # de um perfil de motorista.
        payload = request.get_json()
        err, res = Authorizer.validate(self.access_kind, payload, ['auth'])
        if err:
            return res

        person = self.entity.query.get(uid)
        person_schema = self.schema()
        person_data = person_schema.dump(person)

        addresses = db.session\
            .query(self.addresses)\
            .join(self.entity)\
            .filter(self.entity.uid == uid)\
            .all()

        person_addresses = []
        for rel in addresses:
            person_addresses.append({
                'number': rel.address.number,
                'postcode': rel.address.postcode,
                'complement': rel.address.complement
            })

        person_data = person_data[0]
        person_data['addresses'] = person_addresses
        return response.ok(person_data)

    def put(self):
        pass
