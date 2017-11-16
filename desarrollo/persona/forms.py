from django import forms
from persona.models import *
from django.forms import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

class FormularioIngreso(forms.Form):
    '''
    Corresponde al formulario de ingreso cuando se registra el usuario.
    '''
    cuil = forms.CharField(max_length=15)

    def __init__(self, *args, **kwargs):
        '''
        Función init:
        Se encarga de inicializar el formulario de ingreso.
        :param self: instancia del objeto form.
        :param args: Argumentos que podrían ser necesarios.
        :param kwargs: Mas argumentos.
        :return: Se devuelve el form con la etiqueta: "ingres su nº de cuil".
        '''
        super(FormularioIngreso, self).__init__(*args, **kwargs)
        self.fields['cuil'].widget.attrs['placeholder'] = " Ingrese su nº de cuil"

    def clean_cuil(self):
        '''
        Función clean cuil:
        Se encarga de controlar que no haya errores cuando el usuario ingresa su cuil.
        * Cuil no pertenecea  una Persona.
        * Usuario ya pertenece a una persona
        * El cuil no está registrado
        :param self: instancia del objeto form.
        :return: Se devuelve el cuil validado.
        '''
        cuil= self.cleaned_data['cuil']
        if not Persona.objects.filter(cuil=cuil).exists():
            raise ValidationError("el cuil ingresado no pertenece a una persona")
        if Persona.objects.get(cuil=cuil).usuario:
            raise ValidationError("el usuario ingresado ya pertenece a una persona registrada")
        if not CuilClave.objects.filter(cuil=cuil).exists():
            raise ValidationError("el cuil no está registrado")
        return cuil

    def obtener_o_crear(self, cuil, contraseña):
        '''
        Función obtener o crear:
        Se encarga de verificar los datos del usuario, si no existe, se crea.
        :param self: Instancia del objeto form.
        :param cuil: Cuil ingresado por el agente.
        :param contraseña: Contraseña ingresada por el agente.
        :return: Devuelve el usuario de la persona.
        '''
        persona= Persona.objects.get(cuil= cuil)
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
    '''
    Corresponde al formulario que permite el acceso al sistema por parte del usuario.
    '''
    def __init__(self, *args, **kwargs):
        super(FormularioUsuario, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Cuil"
        self.fields['username'].widget.attrs['placeholder'] = " Ingrese su nº de cuil"
        self.fields['password'].widget.attrs['placeholder'] = " Ingrese su contraseña"

    def clean_cuil(self):
        '''
        Función clean cuil:
        Se encarga de controlar exista en el sistema el cuil ingresado por el usuario.
        :param self: instancia del objeto form.
        :return: Se devuelve el cuil validado.
        '''
        cuil= self.cleaned_data['cuil']
        if not Persona.objects.filter(documento=cuil).exists():
            raise ValidationError("el cuil ingresado no pertenece a una persona")
        return cuil
