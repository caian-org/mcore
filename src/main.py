#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from mapi import app
from mapi import config

from mapi.routes import Router


def main():
    Router.act()
    app.run(debug=config.DEBUG, port=config.PORT)


if __name__ == '__main__':
    main()
