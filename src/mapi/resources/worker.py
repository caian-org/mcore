# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from . import Worker
from . import (Resource, request)


class WorkerAuthentication(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def get(self):
        return { 'hello': 'world' }

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        email = request.form['email']
        worker = Worker.query.filter_by(email=email).all()

        if not worker:
            return {'response': 'nope'}

        return {'name': worker[0].name}
