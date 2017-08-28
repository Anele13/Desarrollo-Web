# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

admin.site.register(Agente)
admin.site.register(Direccion)
admin.site.register(Persona)
admin.site.register(Usuario)
admin.site.register(Administrador)
