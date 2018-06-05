# -*- coding: utf-8 -*-

# ...
from datetime import datetime

# ...
from . import CEP

# Database connection
from . import db
from . import joinedload

# Proposal model
from . import Proposal
from . import Company
from . import Address
from . import Item

# Proposal datatype schema
from . import ProposalSchema
from . import ProposalsListSchema

# HTTP-related
from . import Resource
from . import request
from . import response

# Form/JSON data validator
from .auth import Validator
from .auth import Authorizer


class ProposalResource(Resource):
    def get(self):
        '''
        Implementação do método GET em /proposals/

        Este método é capaz de retornar todas as propostas criadas com status
        "em aberto". Requer autenticação e só pode ser consumido através de uma
        conta corporativa (companu account).
        '''
        payload = request.get_json()
        err, res = Authorizer.validate('company', payload, ['auth'])
        if err:
            return res

        opened_proposals = Proposal.query.filter_by(status=True).all()
        proposal_schema = ProposalsListSchema(many=True)

        data = proposal_schema.dump(opened_proposals)
        return response.ok(data[0])

    def post(self):
        '''
        Implementação do método POST em /proposals/

        Este método é capaz de cadastrar uma proposta mediante indicação dos
        dados necessários. Requer autenticação e só pode ser consumido através
        de uma conta corporativa (company account).
        '''
        payload = request.get_json()
        err, res = Authorizer.validate('company', payload, ['auth', 'data'])
        if err:
            return res

        # Verifica pelas estruturas de endereço de origem e destino
        data = payload['data']
        required_data = ['originAddress', 'destinationAddress']
        if not Validator.check_struct(data, required_data):
            return response.bad_request

        # Verifica pelos campos necessários em cada estrutura
        origin_addr = data['originAddress']
        destin_addr = data['destinationAddress']
        params = [
            data.get('title'),
            data.get('status'),
            data.get('deadline'),
            data.get('companyUid'),
            origin_addr.get('number'),
            origin_addr.get('postcode'),
            destin_addr.get('number'),
            destin_addr.get('postcode')]
        if not Validator.check_payload(params):
            return response.bad_request

        # Verifica se o id recebido é de uma empresa existente
        company = Company.query.get(data['companyUid'])
        if not company:
            return response.bad_request

        # Verifica se existe ao menos um item na lista
        items = data['items']
        if not items:
            return response.bad_request

        # Verifica em cada um dos itens se os atributos necessários constam
        for i in items:
            required_attrs = [
                i.get('title'),
                i.get('width'),
                i.get('height'),
                i.get('weight'),
                i.get('fragile')]
            if not Validator.check_payload(required_attrs):
                return response.bad_request

        # Converte o formato de data 'dd-mm-aaaa' em uma datetime
        data['deadline'] = datetime.strptime(data['deadline'], '%d-%m-%Y')

        # Insere no banco os endereços de origem e destino
        origin = Address(postcode=origin_addr['postcode'],
                         number=origin_addr['number'],
                         complement=origin_addr.get('complement'))

        destin = Address(postcode=destin_addr['postcode'],
                         number=destin_addr['number'],
                         complement=destin_addr.get('complement'))

        db.session.add(origin)
        db.session.add(destin)
        db.session.commit()

        # Insere no banco a proposta
        proposal = Proposal(title=data['title'],
                            status=data['status'],
                            deadline=data['deadline'],
                            description=data.get('description'),
                            origin=origin,
                            destination=destin,
                            company=company)

        db.session.add(proposal)

        # Insere no banco todos os itens, referenciando a proposta
        for i in items:
            item = Item(title=i['title'],
                        width=i['width'],
                        height=i['height'],
                        weight=i['weight'],
                        fragile=i['fragile'],
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


class ProposalOffer(Resource):
    def get(self, uid):
        pass
