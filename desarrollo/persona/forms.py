from django import forms
from persona.models import *
from django.forms import ValidationError
from django.contrib.auth import authenticate
<<<<<<< HEAD
from .models import *
class FormularioUsuario(forms.Form):
=======
from django.contrib.auth.forms import AuthenticationForm

>>>>>>> refs/remotes/origin/master

class FormularioIngreso(forms.Form):
    cuil = forms.IntegerField()
    contraseña = forms.CharField(max_length=15)
    def __init__(self, *args, **kwargs):
        super(FormularioIngreso, self).__init__(*args, **kwargs)
        self.fields['cuil'].widget.attrs['placeholder'] = " Ingrese su nº de cuil"
        self.fields['contraseña'].widget.attrs['placeholder'] = " Ingrese su contraseña"

<<<<<<< HEAD
    def obtener_o_crear(sef,nombreUsuario, contrasenia):
        persona= Persona.objects.get(documento=nombreUsuario)
        if persona.usuario:
            return persona.usuario
        else:
            usuario =  Usuario.objects.create_user(username=nombreUsuario ,password=contrasenia)
            persona.usuario = usuario
            persona.save()
            return persona.usuario
=======
    def clean_cuil(self):
        cuil= self.cleaned_data['cuil']
        if not Persona.objects.filter(documento=cuil).exists():
            raise ValidationError("el cuil ingresado no pertenece a una persona")
        if Persona.objects.get(documento=cuil).usuario:
            raise ValidationError("el usuario ingresado ya pertenece a alguien")
        return cuil

    def obtener_o_crear(self, cuil, contraseña):
        persona= Persona.objects.get(documento= cuil)
        if persona.usuario:
            return persona.usuario
        else:
            agente= Agente()
            agente.save()
            usuario =  Usuario.objects.create_user(username=cuil ,password=contraseña)
            usuario.save()
            persona.agente = agente
            persona.usuario = usuario
            persona.save()
            return persona.usuario


class FormularioUsuario(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioUsuario, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Cuil"
        self.fields['username'].widget.attrs['placeholder'] = " Ingrese su nº de cuil"
        self.fields['password'].widget.attrs['placeholder'] = " Ingrese su contraseña"
>>>>>>> refs/remotes/origin/master

    def clean_cuil(self):
        cuil= self.cleaned_data['cuil']
        if not Persona.objects.filter(documento=cuil).exists():
            raise ValidationError("el cuil ingresado no pertenece a una persona")
        return cuil
