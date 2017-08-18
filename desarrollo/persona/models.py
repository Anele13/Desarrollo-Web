from django.db import models
from .choices import *

class Agente (models.Model):
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


class Direccion(models.Model):
    provincia = models.IntegerField()
    cp = models.CharField(max_length=8)
    localidad = models.CharField(max_length=60)
    calle = models.CharField(max_length=40)
    nro = models.CharField(max_length=6)
    piso = models.CharField(max_length=5)
    dpto = models.CharField(max_length=5)
