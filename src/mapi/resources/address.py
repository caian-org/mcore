# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from . import db
from . import Address
from . import (Resource, request, response)

from .auth import Authenticator


class AddressRecord(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def delete(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass

    def get(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass

    def put(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass


class AddressNew(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        payload = request.get_json()
        if not Authenticator.check_struct(payload, ['auth', 'data']):
            return response.bad_request

        auth  = payload['auth']
        token = auth.get('token')

        data       = payload['data']
        postcode   = data.get('postcode')
        number     = data.get('number')
        complement = data.get('complement')

        params = [token, postcode, number]
        if not Authenticator.check_payload(params):
            return response.bad_request

        if not Authenticator.verify_token(token):
            return response.forbidden

        complement = complement if complement is not None else ''

        address = Address(postcode=postcode,
                          number=number)

        try:
            db.session.add(address)
            db.session.commit()

        except Exception:
            return response.internal_server_error

        addr_uid = address.uid
        return response.address_created(addr_uid)
