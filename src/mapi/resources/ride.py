# -*- coding: utf-8 -*-

# ...
from datetime import datetime

# ...
from . import db

# ...
from . import Ride
from . import Offer

# ...
from . import Resource
from . import request
from . import response

# ...
from .auth import Validator
from .auth import Authorizer


class RideRecord(Resource):
    def post(self):
        payload = request.get_json()
        err, res = Authorizer.validate('company', payload, ['auth', 'data'])
        if err:
            return res

        # Verifica pelas estruturas de endereço de origem e destino
        data = payload['data']
        params = [data.get('offerId')]
        if not Validator.check_payload(params):
            return response.bad_request

        # Pesquisa e armazena o objeto da oferta
        offer = Offer.query.get(data['offerId'])

        # Verifica se a oferta existe
        if not offer:
            return response.not_found

        # Cria a corrida no banco
        ride = Ride(
            offer=offer,
            start_date=datetime.now()
        )

        db.session.add(ride)
        db.session.commit()

        return response.created('rides', ride.uid)
