# -*- coding: utf-8 -*-

from mapi import app


@app.route('/')
def index():
    return 'hello world!'
