# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

import sys


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
