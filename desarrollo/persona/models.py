# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from .choices import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    piso = models.CharField(max_length=5, null=True, blank=True)
    dpto = models.CharField(max_length=5, null = True, blank=True )
    extra= models.CharField(max_length=5)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
