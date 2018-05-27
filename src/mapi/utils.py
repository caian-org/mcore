# -*- coding: utf-8 -*-

import sys

from mapi import __version__
from mapi import __parent_resource__


class Exit:
    @staticmethod
    def with_success(message):
        print(message)
        sys.exit(0)

    @staticmethod
    def with_fail(message):
        print(message)
        sys.exit(1)

    @staticmethod
    def SIGINT():
        Exit.with_success('\n\nSIGINT caught. Exiting gracefully...')


class Formatter:
    @staticmethod
    def gen_route(resource):
        return '/{0}/{1}/{2}'.format(__parent_resource__, __version__, resource)
