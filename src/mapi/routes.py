# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from mapi import rapi
from mapi import __version__
from mapi import __parent_resource__

from mapi.resources.worker import WorkerAuthentication


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
