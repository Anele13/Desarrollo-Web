from __future__ import unicode_literals
from django.db import models
from .choices import *
from django.contrib.auth.models import AbstractUser, Group
from liquidacion.models import *

class CuilClave(models.Model):
    '''
    Corresponde a las claves de los usuarios en primer instancia.
    '''
    clave= models.CharField(max_length=20)
    cuil= models.CharField(max_length=20)
    id = models.AutoField(auto_created=True,primary_key=True, blank=True)


class Rol(models.Model):
    '''
    Clase abstracta, corresponde a los roles existentes en el sistema.
    '''
    class Meta:
        abstract= True


class Agente(Rol):
    '''
    Corresponde al rol de agente.
    '''
    def get_view_name(self):
        '''
        Función get view name:
        Se encarga de devolver el nombre del rol actuante.
        :param self: instancia del objeto rol.
        :return: Se devuelve el tipo de rol.
        '''
        return "Agente"


class Administrador(Rol):
    '''
    Corresponde al rol de administrador.
    '''
    def get_view_name(self):
        '''
        Función get view name:
        Se encarga de devolver el nombre del rol actuante.
        :param self: instancia del objeto rol.
        :return: Se devuelve el tipo de rol.
        '''
        return "Administrador"

    def __str__(self):
        return "%s " % (self.id)


class Usuario(Rol, AbstractUser):
    '''
    Corresponde al usuario, como rol, hasta el momento puede ser agente o administrador.
    '''
    AGENTE = "AGENTE"
    ADMINISTRADOR = "ADMINISTRADOR"

    def get_view_name(self):
        '''
        Función get view name:
        Se encarga de devolver el nombre del rol actuante.
        :param self: instancia del objeto rol.
        :return: Se devuelve el tipo de rol.
        '''
        return self.groups.first().name

    def get_view_groups(self):
        '''
        Función get view group:
        Se encarga de devolver el nombre del grupo al que pertenece el usuario.
        :param self: instancia del objeto rol.
        :return: Se devuelve el tipo de grupo.
        '''
        return self.groups.all()


class Persona(models.Model):
    '''
    Corresponde a los datos de la persona registrados en el sistema.
    '''
    documento = models.BigIntegerField(primary_key=True)
    nya= models.CharField(max_length=30)
    empliq=models.CharField(max_length=10, null=True, blank=True)
    sexo= models.CharField(max_length=2, choices=Sexo, null=True, blank=True)
    cuil= models.CharField(max_length=15, null=True, blank=True)
    f572= models.IntegerField(null=True, blank=True)
    fechaf572= models.DateField(null=True, blank=True)
    observ= models.CharField(max_length=255, null=True, blank=True)
    fechapres= models.DateField(null=True, blank=True)
    nropres= models.IntegerField(null=True, blank=True)
    famok= models.IntegerField(null=True, blank=True)
    excep= models.IntegerField(null=True, blank=True)
    web= models.IntegerField(null=True, blank=True)
    fechaweb= models.DateField(null=True, blank=True)
    wcuit= models.CharField(max_length=15, null=True, blank=True)
    wtipodoc= models.CharField(max_length=5, choices=Tipo, null=True, blank=True)
    wapellido= models.CharField(max_length=50, null=True, blank=True)
    wnombre= models.CharField(max_length=50, null=True, blank=True)
    wdireccion= models.CharField(max_length=50, null=True, blank=True)
    wprovincia= models.CharField(max_length=50, null=True, blank=True)
    wcp= models.CharField(max_length=30, null=True, blank=True)
    wlocalidad= models.CharField(max_length=60, null=True, blank=True)
    wcalle= models.CharField(max_length=40, null=True, blank=True)
    wnro= models.CharField(max_length=10, null=True, blank=True)
    wpiso= models.CharField(max_length=10, null=True, blank=True)
    wdpto= models.CharField(max_length=10, null=True, blank=True)
    wcuitreten= models.CharField(max_length=20, null=True, blank=True)
    wdescreten= models.CharField(max_length=200, null=True, blank=True)
    periodo= models.IntegerField(null=True, blank=True)
    revisado= models.CharField(max_length=10, null=True, blank=True)
    agente= models.OneToOneField(Agente, blank=True, null=True, on_delete=models.CASCADE)
    administrador= models.OneToOneField(Administrador, blank=True, null=True, on_delete=models.CASCADE)
    usuario = models.OneToOneField(Usuario, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s " % (self.documento)
