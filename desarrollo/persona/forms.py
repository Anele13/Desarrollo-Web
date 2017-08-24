from django import forms
from persona.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormularioUsuario(forms.Form):
    Cuil = forms.CharField()
    Contraseña = forms.CharField()

    def obtener_o_crear(nombreUsuario, contraseña):
        persona= Persona.objects.get(documento=nombreUsuario)
        if persona.usuario:
            return persona.usuario
        else:
             usuario =  Usuario.objects.create_user(username=nombreUsuario ,password=contraseña)
             persona.usuario = usuario
             persona.save()
             return persona.usuario
