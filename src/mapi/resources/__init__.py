# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

# Standard libraries
import sys
from os import path

# 3rd-party libraries
from flask import request
from flask_restful import Resource


# Parent directory "injection"
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


# Models module
from mapi.models import *
