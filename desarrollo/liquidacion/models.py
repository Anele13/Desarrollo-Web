# -*- coding: utf-8 -*-
from django.db import models
from persona import models as p
# Create your models here.
from django.db import models

class Concepto(models.Model):
    descrip = models.CharField(max_length=150, null=True)
    prorratea = models.FloatField(null=True)
    orden = models.IntegerField(null=True)
    grupo = models.IntegerField(null=True)
    modulo = models.IntegerField(null=True)
    topepro = models.FloatField(null=True)
    signo = models.CharField(max_length=150, null=True)
    concepto = models.CharField(max_length=10, primary_key=True)
    grupotope = models.CharField(max_length=10, null=True)
    muestraliq = models.IntegerField(null=True)
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
    mes = models.ForeignKey(Mes, on_delete=models.CASCADE, db_column='mes')
    indice = models.IntegerField()
    descrip = models.CharField(max_length=50)
    cierre = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.liqnro, self.fecha)


class Hliquidac(models.Model):
    documento = models.ForeignKey(p.Persona, on_delete=models.CASCADE, db_column='documento')
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE, db_column='concepto')
    monto = models.FloatField(null=True)
    nroliq = models.ForeignKey(Cabliq, on_delete=models.CASCADE, db_column='nroliq')
    mes = models.ForeignKey(Mes, on_delete=models.CASCADE, null=True, db_column='mes')
    id = models.AutoField(auto_created=True,primary_key=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.nroliq, self.documento)


class Empresa(models.Model):
    codemp = models.IntegerField(primary_key=True)         #CONSULTA POR EL REPETIDO
    saf = models.IntegerField(null=True)
    descrip = models.CharField(max_length=50, null=True)
    claveseg = models.CharField(max_length=50, null=True)
    codtipo = models.IntegerField(null=True)
    excep = models.IntegerField(null=True)
    safcentral = models.IntegerField(null=True)
    cuit = models.CharField(max_length=13,null=True)
    calle = models.CharField(max_length=30,null=True)
    nro = models.IntegerField(null=True)
    codsicore = models.IntegerField(null=True)
    empresue = models.CharField(max_length=2,null=True)
    activo = models.IntegerField(null=True)
    administrador_Responsable = models.ForeignKey(p.Administrador, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.codemp


class PersonaEmp(models.Model):
    documento = models.ForeignKey(p.Persona, on_delete=models.CASCADE, db_column='documento')
    codemp = models.ForeignKey(Empresa, db_index=True, on_delete=models.CASCADE, db_column='codemp')
    totalhab = models.FloatField(null=True)
    id = models.AutoField(auto_created=True,primary_key=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.codemp, self.documento)


class LiqFin(models.Model):
    DESCRIP = models.CharField(max_length=100, null=True)
    PERIODO= models.IntegerField(null=True, blank=True)
    ECUIT = models.CharField(max_length=15, null=True, blank=True)
    DOCUMENTO = models.BigIntegerField(primary_key=True)
    NYA = models.CharField(max_length=30)
    EMPLIQ = models.CharField(max_length=10, null=True, blank=True)
    NYA2 = models.CharField(max_length=30)
    CUIT = models.CharField(max_length=15, null=True, blank=True)
    WCALLE = models.CharField(max_length=40, null=True, blank=True)
    WNRO = models.CharField(max_length=10, null=True, blank=True)
    WPISO = models.CharField(max_length=10, null=True, blank=True)
    WDPTO = models.CharField(max_length=10, null=True, blank=True)
    WLOCALIDAD = models.CharField(max_length=60, null=True, blank=True)
    WPROVINCIA = models.CharField(max_length=50, null=True, blank=True)
    WCP = models.CharField(max_length=30, null=True, blank=True)
    '''
     Monto charfield porque postgres trabaja solamente con formato EE.UU
     se consideró que no se realizan operaciones con los datos
    '''
    R01_00 =  models.CharField(max_length=50, null=True, blank=True)
    R01A00 =  models.CharField(max_length=50, null=True, blank=True)
    R01B00 =  models.CharField(max_length=50, null=True, blank=True)
    R01C00 =  models.CharField(max_length=50, null=True, blank=True)
    R01D00 =  models.CharField(max_length=50, null=True, blank=True)
    R01Z00 =  models.CharField(max_length=50, null=True, blank=True)
    R02_00 =  models.CharField(max_length=50, null=True, blank=True)
    R02A00 =  models.CharField(max_length=50, null=True, blank=True)
    R02B00 =  models.CharField(max_length=50, null=True, blank=True)
    R02C00 =  models.CharField(max_length=50, null=True, blank=True)
    R02D00 =  models.CharField(max_length=50, null=True, blank=True)
    R02E00 =  models.CharField(max_length=50, null=True, blank=True)
    R02F00 =  models.CharField(max_length=50, null=True, blank=True)
    R02G00 =  models.CharField(max_length=50, null=True, blank=True)
    R02H00 =  models.CharField(max_length=50, null=True, blank=True)
    R02I00 =  models.CharField(max_length=50, null=True, blank=True)
    R02J00 =  models.CharField(max_length=50, null=True, blank=True)
    R02K00 =  models.CharField(max_length=50, null=True, blank=True)
    R02L00 =  models.CharField(max_length=50, null=True, blank=True)
    R02M00 =  models.CharField(max_length=50, null=True, blank=True)
    R02N00 =  models.CharField(max_length=50, null=True, blank=True)
    R02O00 =  models.CharField(max_length=50, null=True, blank=True)
    R02P00 =  models.CharField(max_length=50, null=True, blank=True)
    R02Q00 =  models.CharField(max_length=50, null=True, blank=True)
    R02Z00 =  models.CharField(max_length=50, null=True, blank=True)
    R03_00 =  models.CharField(max_length=50, null=True, blank=True)
    R03A00 =  models.CharField(max_length=50, null=True, blank=True)
    R03B00 =  models.CharField(max_length=50, null=True, blank=True)
    R03C00 =  models.CharField(max_length=50, null=True, blank=True)
    R03D00 =  models.CharField(max_length=50, null=True, blank=True)
    R03E00 =  models.CharField(max_length=50, null=True, blank=True)
    R03Z00 =  models.CharField(max_length=50, null=True, blank=True)
    R04_00 =  models.CharField(max_length=50, null=True, blank=True)
    R04A00 =  models.CharField(max_length=50, null=True, blank=True)
    R04B00 =  models.CharField(max_length=50, null=True, blank=True)
    R04C00 =  models.CharField(max_length=50, null=True, blank=True)
    R04Z00 =  models.CharField(max_length=50, null=True, blank=True)
    SALDO  =  models.CharField(max_length=50, null=True, blank=True)
    SALDOAFIP =  models.CharField(max_length=50, null=True, blank=True)
    SALDOBEN =  models.CharField(max_length=50, null=True, blank=True)
