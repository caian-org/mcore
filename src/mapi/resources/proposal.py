# -*- coding: utf-8 -*-

# ...
from datetime import datetime

# Database connection
from . import db

# Proposal model
from . import Proposal
from . import Company
from . import Address
from . import Item

# Proposal datatype schema
from . import ProposalSchema

# HTTP-related
from . import Resource
from . import request
from . import response

# Form/JSON data authenticator
from .auth import Authenticator


class ProposalNew(Resource):
    def post(self):
        payload = request.get_json()

        # Verifica a estrutura da payload recebida
        if not Authenticator.check_struct(payload, ['auth', 'data']):
            return response.bad_request

        # Verifica se o token é valido
        auth = payload['auth']
        token = auth.get('token')
        if not Authenticator.verify_token(token):
            return response.forbidden

        # Verifica pelas estruturas de endereço de origem e destino
        data = payload['data']
        required_data = ['originAddress', 'destinationAddress']
        if not Authenticator.check_struct(data, required_data):
            return response.bad_request

        # Verifica pelos campos necessários em cada estrutura
        origin_addr = data['originAddress']
        destin_addr = data['destinationAddress']
        params = [
            data.get('deadline'),
            data.get('companyUid'),
            origin_addr.get('number'),
            origin_addr.get('postcode'),
            destin_addr.get('number'),
            destin_addr.get('postcode')]
        if not Authenticator.check_payload(params):
            return response.bad_request

        # Verifica se existe ao menos um item na lista
        items = data['items']
        if not items:
            return response.bad_request

        # Verifica em cada um dos itens se os atributos necessários constam
        for i in items:
            required_attrs = [
                i.get('fragile'),
                i.get('weight'),
                i.get('width'),
                i.get('height')]
            if not Authenticator.check_payload(required_attrs):
                return response.bad_request

        # Converte o formato de data 'dd-mm-aaaa' em uma datetime
        data['deadline'] = datetime.strptime(data['deadline'], '%d-%m-%Y')

        # Verifica se o id recebido é de uma empresa existente
        company = Company.query.get(data['companyUid'])
        if not company:
            return response.bad_request

        # Insere no banco os endereços de origem e destino
        origin = Address(postcode=origin_addr['postcode'],
                         number=origin_addr['number'],
                         complement=origin_addr['complement'])

        destin = Address(postcode=destin_addr['postcode'],
                         number=destin_addr['number'],
                         complement=destin_addr['complement'])

        db.session.add(origin)
        db.session.add(destin)
        db.session.commit()

        # Insere no banco a proposta
        proposal = Proposal(deadline=data['deadline'],
                            origin=origin,
                            destination=destin,
                            company=company)

        db.session.add(proposal)

        # Insere no banco todos os itens, referenciando a proposta
        for i in items:
            item = Item(fragile=i['fragile'],
                        weight=i['weight'],
                        width=i['width'],
                        height=i['height'],
                        proposal=proposal)

            db.session.add(item)

        db.session.commit()

        return response.created('proposals', proposal.uid)

class ProposalRecord(Resource):
    def delete(self):
        pass

    def get(self):
        pass

    def put(self):
        pass


class ProposalOffers(Resource):
    pass
