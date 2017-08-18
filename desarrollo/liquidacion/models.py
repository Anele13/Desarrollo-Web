from django.db import models

# Create your models here.
class Hliquidac(models.Model):
    documento = models.IntegerField()
    concepto = models.CharField(max_length=10)
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
