from __future__ import unicode_literals
from django.db import models
from .choices import *
from django.contrib.auth.models import AbstractUser, Group

class Rol(models.Model):
    class Meta:
        abstract= True


class Agente(Rol):
     def get_view_name(self):
        return "Agente"


class Administrador(Rol):
     def get_view_name(self):
        return "Administrador"


class Usuario(Rol, AbstractUser):
    AGENTE = "AGENTE"
    ADMINISTRADOR = "ADMINISTRADOR"
    
    def get_view_name(self):
        return self.groups.first().name

    def get_view_groups(self):
        return self.groups.all()


class Persona(models.Model):
    documento  = models.BigIntegerField()
    tipo_doc = models.CharField(max_length=10, choices=Tipo)
    #nya #NOMBRE Y APELLIDO, O NYA?
    empliq = models.IntegerField()
    sexo = models.CharField(max_length=1)
    cuil = models.CharField(max_length=15)
    f572 = models.IntegerField ()
    fecha_f572 = models.DateField()
    fecha_aplic  = models.DateField()
    observ = models.CharField(max_length=255)
    direccion = models.ForeignKey('Direccion', on_delete=models.CASCADE)
    revisado = models.CharField(max_length=10)
    usuario = models.OneToOneField(Usuario, blank=True, null=True)

    def crear_usuario(self, nombre, clave):
        self.usuario = Usuario.objects.create_user(username=nombre, password=clave)

class Direccion(models.Model):
    provincia = models.IntegerField()
    cp = models.CharField(max_length=8)
    localidad = models.CharField(max_length=60)
    calle = models.CharField(max_length=40)
    nro = models.CharField(max_length=6)
    piso = models.CharField(max_length=5)
    dpto = models.CharField(max_length=5)
