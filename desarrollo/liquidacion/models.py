# -*- coding: utf-8 -*-
from django.db import models
from persona import models as p
# Create your models here.

class Concepto(models.Model):
    descrip = models.CharField(max_length=150, null=True)
    proratea = models.FloatField(null=True)
    orden = models.IntegerField(null=True)
    grupo = models.IntegerField(null=True)
    modulo = models.IntegerField(null=True)
    topepro = models.FloatField(null=True)
    signo = models.CharField(max_length=150, null=True)
    concepto = models.CharField(max_length=10, primary_key=True)
    grupotope = models.CharField(max_length=10, null=True)
    muestra_liq = models.IntegerField(null=True)
    anexas = models.IntegerField(null=True)
    vista = models.IntegerField(null=True)
    titulo = models.IntegerField(null=True)
    of649 = models.CharField(max_length=150, null=True)
    ordenliq = models.CharField(max_length=150, null=True)
    fliqfin = models.CharField(max_length=150, null=True)
    grupolf = models.IntegerField(null=True)
    ldescrip = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "%s" % self.descrip

class Mes(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return "%s" % self.nombre


class Cabliq(models.Model):
    liqnro = models.IntegerField(primary_key=True)
    fecha = models.DateField()
    mes = models.ForeignKey(Mes, on_delete=models.CASCADE)
    indice = models.IntegerField()
    descrip = models.CharField(max_length=50)
    cierre = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.liqnro, self.fecha)


class Hliquidac(models.Model):
    documento = models.ForeignKey(p.Persona, on_delete=models.CASCADE)
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE)
    monto = models.FloatField(null=True)
    nro_liq = models.ForeignKey(Cabliq, on_delete=models.CASCADE)
    mes = models.ForeignKey(Mes, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s - %s" % (self.nro_liq, self.documento)


class Empresa(models.Model):
    cod_emp = models.IntegerField(primary_key=True)
    saf = models.IntegerField(null=True)
    descrip = models.CharField(max_length=50, null=True)
    clave_seg = models.CharField(max_length=50, null=True)
    cod_tipo = models.IntegerField(null=True)
    excep = models.IntegerField(null=True)
    saf_central = models.IntegerField(null=True)
    cuit = models.CharField(max_length=13,null=True)
    calle = models.CharField(max_length=30,null=True)
    nro = models.IntegerField(null=True)
    cod_sicore = models.IntegerField(null=True)
    empresue = models.CharField(max_length=2,null=True)
    activo = models.IntegerField(null=True)

    def __str__(self):
        return "%s" % self.cod_emp


class PersonaEmp(models.Model):
    documento = models.ForeignKey(p.Persona, on_delete=models.CASCADE)
    codemp = models.ForeignKey(Empresa, db_index=True, on_delete=models.CASCADE)
    totalhab = models.FloatField(null=True)

    def __str__(self):
        return "%s - %s" % (self.codemp, self.documento)
