# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from mapi import app


@app.route('/')
def index():
    return 'hello world!'
