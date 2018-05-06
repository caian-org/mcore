#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from mapi import app
from mapi import Config

from mapi.routes import Router


def main():
    Router.act()
    app.run(debug=Config.DEBUG, port=Config.PORT)


if __name__ == '__main__':
    main()
