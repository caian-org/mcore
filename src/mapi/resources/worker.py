# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from . import Worker
from . import (Response, Resource, request)


class WorkerAuthentication(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        email = request.form['email']
        worker = Worker.query.filter_by(email=email).all()

        if not worker:
            error = { 'description': 'User not found' }
            return Response.FAIL(404, error)

        data = {}
        data['worker'] = { 'name': worker[0].name }
        return Response.SUCCESS(200, data)


class WorkerRegistry(Resource):
    pass
