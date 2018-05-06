# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

import sys
from os import path


# Parent directory "injection"
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from mapi.utils import Exit
from mapi.models import *

try:
    from flask import request
    from flask_restful import Resource

except ImportError as error:
    Exit.with_fail('Impossible to import 3rd-party libraries\n'
                   'Latest traceback: {0}' . format(error.args[0]))

from mapi.resources.responder import Response
