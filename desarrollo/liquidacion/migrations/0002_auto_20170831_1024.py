# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liquidacion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='activo',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='calle',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='clave_seg',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='cod_sicore',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='cod_tipo',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='cuit',
            field=models.CharField(max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='descrip',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='empresue',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='excep',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='nro',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='saf',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='saf_central',
            field=models.IntegerField(null=True),
        ),
    ]