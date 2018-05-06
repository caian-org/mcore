# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

import sys
from os import path


# Parent directory "injection"
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from mapi import (request, Resource, BadRequest)

from mapi.utils import Exit
from mapi.models import *

from mapi.resources.responder import response
