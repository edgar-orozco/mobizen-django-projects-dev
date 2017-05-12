# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0002_auto_20151005_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccion',
            name='latitud',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=15, blank=True),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='longitud',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=15, blank=True),
        ),
    ]
