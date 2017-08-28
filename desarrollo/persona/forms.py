from django import forms
from persona.models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from django.contrib.auth import authenticate

class FormularioUsuario(forms.Form):

    cuil = forms.CharField()
    contrasenia = forms.CharField(widget=forms.PasswordInput)

    def obtener_o_crear(sef,nombreUsuario, contrasenia):
        persona= Persona.objects.get(documento=nombreUsuario)
        if persona.usuario:
            return persona.usuario
        else:
             usuario =  Usuario.objects.create_user(username=nombreUsuario ,password=contrasenia)
             persona.usuario = usuario
             persona.save()
             return persona.usuario

    def clean_cuil(self):
        cuil= self.cleaned_data['cuil']
        if not Persona.objects.filter(documento=cuil).exists():
            raise ValidationError("el cuil ingresado no pertenece a una persona")
        return cuil

    def clean_contrasenia(self):
        cuil= self.cleaned_data['cuil']
        contra= self.cleaned_data['contrasenia']
        persona= Persona.objects.get(documento=cuil)
        if not persona.Usuario.check_password(contra):
            raise ValidationError("le contrasenia no le pertenece al usuario")
