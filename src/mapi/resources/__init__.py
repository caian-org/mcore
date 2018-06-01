# -*- coding: utf-8 -*-

import sys
from os import path


# Parent directory "injection"
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from mapi import db         # ORM & Objeto de conexão do banco
from mapi import config     # Objeto de configurações do servidor & banco
from mapi import request    # Objeto de requisição HTTP do Flask
from mapi import Resource   # Classe de recurso REST
from mapi import Formatter  # Classe utilitária para formatação de rotas REST
from mapi import joinedload # Clausula de combinação entre modelos (JOIN)

from mapi.models import *
from mapi.schemas import *

from mapi.resources.responder import response
