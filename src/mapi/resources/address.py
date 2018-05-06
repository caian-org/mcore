# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from . import db
from . import Address
from . import (Resource, request, response)


class AddressInclusion(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        postcode   = request.form.get('postcode')
        number     = request.form.get('number')
        complement = request.form.get('complement')

        if not postcode or not number:
            return response.bad_request

        # complement = complement if complement is not None else ''

        address = Address(postcode=postcode,
                          number=number,
                          complement=complement)

        try:
            db.session.add(address)
            db.session.commit()

        except Exception:
            return response.internal_server_error

        addr_uid = address.uid
        return response.address_created(addr_uid)
