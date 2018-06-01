# -*- coding: utf-8 -*-

from mapi import db
from mapi import mars


# Tipos primitivos
Bool  = db.Boolean
Dat   = db.DateTime
Float = db.Float
Int   = db.Integer
Str   = db.String

# Entidades & Objetos
Col   = db.Column
Model = db.Model

# Relacionamentos
BR  = db.backref
FK  = db.ForeignKey
Rel = db.relationship

# Sessão do ORM
session = db.session


# Classes do Marshmallow
Schema = mars.ModelSchema
Nested = mars.Nested
