from django import forms
from persona.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

class FormularioUsuario(forms.Form):
    cuil = forms.CharField()
    contraseña = forms.CharField()

    def obtener_o_crear(nombreUsuario, contraseña):
        persona= Persona.objects.get(documento=nombreUsuario)
        if persona.usuario:
            return persona.usuario
        else:
             usuario =  Usuario.objects.create_user(username=nombreUsuario ,password=contraseña)
             persona.usuario = usuario
             persona.save()
             return persona.usuario

    def clean_cuil(self):
        cuil= self.cleaned_data['cuil']
        if not Persona.objects.filter(documento=cuil).exists():
            raise ValidationError("el cuil ingresado no pertenece a una persona")
        if Persona.objects.get(documento=cuil).usuario:
            raise ValidationError("El cuil ingresado ya le pertenece a alguien")
        return cuil
