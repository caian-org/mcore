# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from mapi import (rapi, Resource)
from mapi import __version__
from mapi import __parent_resource__

from mapi.models import Worker


class WorkerAuthentication(Resource):
    """
    --- TODO: DOCUMENTATION ---
    """

    def post(self):
        """
        --- TODO: DOCUMENTATION ---
        """
        pass

class Router:
    """
    --- TODO: DOCUMENTATION ---
    """

    @staticmethod
    def format(route):
        """
        --- TODO: DOCUMENTATION ---
        """
        return '/{0}/{1}/{2}'.format(__parent_resource__, __version__, route)

    @staticmethod
    def act():
        """
        --- TODO: DOCUMENTATION ---
        """
        rapi.add_resource(WorkerAuthentication, Router.format('workers/auth'))
