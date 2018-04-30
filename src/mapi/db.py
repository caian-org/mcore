# -*- coding: utf-8 -*-

from mapi import db

# Primitive types
Bol = db.Boolean
Dat = db.DateTime
Flo = db.Float
Int = db.Integer
Str = db.String

# Objects
Col = db.Column
Mod = db.Model

# Relations
BR = db.backref
FK = db.ForeignKey
Rel = db.relationship

# Session
session = db.session
