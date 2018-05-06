# -*- coding: utf-8 -*-

"""
--- TODO: DOCUMENTATION ---
"""

from mapi import db

# Primitive types
Bool  = db.Boolean
Dat   = db.DateTime
Float = db.Float
Int   = db.Integer
Str   = db.String

# Objects
Col   = db.Column
Model = db.Model

# Relations
BR  = db.backref
FK  = db.ForeignKey
Rel = db.relationship

# Session
session = db.session
