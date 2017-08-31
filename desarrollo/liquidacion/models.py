# -*- coding: utf-8 -*-
from django.db import models
from persona import models as p
# Create your models here.

class Concepto(models.Model):
    descrip = models.CharField(max_length=50)
    proratea = models.IntegerField()
    orden = models.IntegerField()
    grupo = models.IntegerField()
    modulo = models.IntegerField()
    topepro = models.IntegerField()
    signo = models.FloatField()
    concepto = models.CharField(max_length=10, primary_key=True)
    grupotope = models.CharField(max_length=10)
    muestra_liq = models.IntegerField()
    anexas = models.IntegerField()
    vista = models.IntegerField()
    titulo = models.IntegerField()
    of649 = models.CharField(max_length=6)
    ordenliq = models.CharField(max_length=6)
    fliqfin = models.CharField(max_length=6)
    grupolf = models.IntegerField()
    ldescrip = models.CharField(max_length=6)

    def __str__(self):
        return "%s" % self.descrip

class Mes(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return "%s" % self.nombre


class Hliquidac(models.Model):
    documento = models.ForeignKey(p.Persona, on_delete=models.CASCADE)
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE)
    monto = models.FloatField()
    nro_liq = models.BigIntegerField()
    mes = models.ForeignKey(Mes, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.nro_liq, self.documento)


class Empresa(models.Model):
    cod_emp = models.IntegerField(primary_key=True)
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
        return "%s" % self.cod_emp


class PersonaEmp(models.Model):
    documento = models.ForeignKey(p.Persona, on_delete=models.CASCADE)
    codemp = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    totalhab = models.FloatField()
