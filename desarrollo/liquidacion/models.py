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
    descrip = models.CharField(max_length=100, null=True)
    periodo= models.IntegerField(null=True, blank=True)
    ecuit = models.CharField(max_length=100, null=True, blank=True)
    documento = models.BigIntegerField(primary_key=True)
    nya = models.CharField(max_length=100)
    empliq = models.CharField(max_length=100, null=True, blank=True)
    cuit = models.CharField(max_length=100, null=True, blank=True)
    wcalle = models.CharField(max_length=100, null=True, blank=True)
    wnro = models.CharField(max_length=100, null=True, blank=True)
    wpiso = models.CharField(max_length=100, null=True, blank=True)
    wdpto = models.CharField(max_length=100, null=True, blank=True)
    wlocalidad = models.CharField(max_length=100, null=True, blank=True)
    wprovincia = models.CharField(max_length=100, null=True, blank=True)
    wcp = models.CharField(max_length=100, null=True, blank=True)
    '''
     Monto charfield porque postgres trabaja solamente con formato EE.UU
     se consideró que no se realizan operaciones con los datos

     detalle:
     se agrega length 100 por el largo de los campos que aparecen nuevos
    '''
    r01_00 =  models.CharField(max_length=100, null=True, blank=True)
    r01a00 =  models.CharField(max_length=100, null=True, blank=True)
    r01b00 =  models.CharField(max_length=100, null=True, blank=True)
    r01c00 =  models.CharField(max_length=100, null=True, blank=True)
    r01d00 =  models.CharField(max_length=100, null=True, blank=True)
    r01z00 =  models.CharField(max_length=100, null=True, blank=True)
    r02_00 =  models.CharField(max_length=100, null=True, blank=True)
    r02a00 =  models.CharField(max_length=100, null=True, blank=True)
    r02b00 =  models.CharField(max_length=100, null=True, blank=True)
    r02c00 =  models.CharField(max_length=100, null=True, blank=True)
    r02d00 =  models.CharField(max_length=100, null=True, blank=True)
    r02e00 =  models.CharField(max_length=100, null=True, blank=True)
    r02f00 =  models.CharField(max_length=100, null=True, blank=True)
    r02g00 =  models.CharField(max_length=100, null=True, blank=True)
    r02h00 =  models.CharField(max_length=100, null=True, blank=True)
    r02i00 =  models.CharField(max_length=100, null=True, blank=True)
    r02j00 =  models.CharField(max_length=100, null=True, blank=True)
    r02k00 =  models.CharField(max_length=100, null=True, blank=True)
    r02l00 =  models.CharField(max_length=100, null=True, blank=True)
    r02m00 =  models.CharField(max_length=100, null=True, blank=True)
    r02n00 =  models.CharField(max_length=100, null=True, blank=True)
    r02o00 =  models.CharField(max_length=100, null=True, blank=True)
    r02p00 =  models.CharField(max_length=100, null=True, blank=True)
    r02q00 =  models.CharField(max_length=100, null=True, blank=True)
    r02z00 =  models.CharField(max_length=100, null=True, blank=True)
    r03_00 =  models.CharField(max_length=100, null=True, blank=True)
    r03a00 =  models.CharField(max_length=100, null=True, blank=True)
    r03b00 =  models.CharField(max_length=100, null=True, blank=True)
    r03c00 =  models.CharField(max_length=100, null=True, blank=True)
    r03d00 =  models.CharField(max_length=100, null=True, blank=True)
    r03e00 =  models.CharField(max_length=100, null=True, blank=True)
    r03z00 =  models.CharField(max_length=100, null=True, blank=True)
    r04_00 =  models.CharField(max_length=100, null=True, blank=True)
    r04a00 =  models.CharField(max_length=100, null=True, blank=True)
    r04b00 =  models.CharField(max_length=100, null=True, blank=True)
    r04c00 =  models.CharField(max_length=100, null=True, blank=True)
    r04z00 =  models.CharField(max_length=100, null=True, blank=True)
    saldo  =  models.CharField(max_length=100, null=True, blank=True)
    saldoafip =  models.CharField(max_length=100, null=True, blank=True)
    saldoben =  models.CharField(max_length=100, null=True, blank=True)
