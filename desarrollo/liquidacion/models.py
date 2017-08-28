# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Concepto(models.Model):
    descrip = models.CharField(max_length=50)
    proratea = models.IntegerField()
    orden = models.IntegerField()
    grupo = models.IntegerField()
    modulo = models.IntegerField()
    topepro = models.IntegerField()
    signo = models.IntegerField()
    concepto = models.CharField(max_length=10)
    grupotope = models.IntegerField()
    muestra_liq = models.IntegerField()
    anexas = models.IntegerField()
    vista = models.IntegerField()
    titulo = models.IntegerField()
    of649 = models.CharField(max_length=6)
    ordenliq = models.CharField(max_length=6)
    fliqfin = models.CharField(max_length=6)
    grupolf = models.IntegerField()
    ldescrip = models.CharField(max_length=6)


class Hliquidac(models.Model):
    documento = models.IntegerField()
    concepto = models.CharField(max_length=10) #APUNTA A CLASE CONCEPTO?
    monto = models.FloatField()
    nro_liq = models.BigIntegerField()
    mes = models.IntegerField()


class Empresa(models.Model):
    cod_emp = models.IntegerField()
    saf = models.IntegerField()
    descrip = models.CharField(max_length=50)
    clave_seg = models.CharField(max_length=50)
    cod_tipo = models.IntegerField()
    excep = models.IntegerField()
    saf_central = models.IntegerField()
    cuit = models.CharField(max_length=13)
    calle = models.CharField(max_length=30)
    nro = models.IntegerField()
    cod_sicore = models.IntegerField()
    empresue = models.CharField(max_length=2)
    activo = models.IntegerField()

    def __str__(self):
        return "soy empresa nº"+str(self.cod_emp)
