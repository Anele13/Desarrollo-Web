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
<<<<<<< HEAD
    #saf= models.ForeignKey(Empresa,blank=True, null=True, on_delete=models.CASCADE)
    pass
    '''
=======
    #saf= models.ForeignKey(Empresa,blank=True, null=True)

>>>>>>> refs/remotes/origin/master
    def get_saf():
        return self.saf
    '''

class Usuario(Rol, AbstractUser):
    AGENTE = "AGENTE"
    ADMINISTRADOR = "ADMINISTRADOR"

    def get_view_name(self):
        return self.groups.first().name

    def get_view_groups(self):
        return self.groups.all()

class Persona(models.Model):
<<<<<<< HEAD
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
=======
    documento  = models.BigIntegerField()
    tipo_doc = models.CharField(max_length=10, choices=Tipo)
    agente= models.OneToOneField(Agente, blank=True, null=True)
    administrador= models.OneToOneField(Administrador, blank=True, null=True)
    usuario = models.OneToOneField(Usuario, blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.documento, self.usuario)
>>>>>>> refs/remotes/origin/master


'''
class Direccion(models.Model):
    provincia = models.IntegerField()
    cp = models.CharField(max_length=8)
    localidad = models.CharField(max_length=60)
    calle = models.CharField(max_length=40)
    nro = models.CharField(max_length=6)
    piso = models.CharField(max_length=5, null=True, blank=True)
    dpto = models.CharField(max_length=5, null = True, blank=True )
    extra= models.CharField(max_length=5)
'''
