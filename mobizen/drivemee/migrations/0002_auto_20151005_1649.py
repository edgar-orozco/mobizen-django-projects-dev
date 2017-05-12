# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccion',
            name='latitud',
            field=models.DecimalField(null=True, max_digits=13, decimal_places=9, blank=True),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='longitud',
            field=models.DecimalField(null=True, max_digits=13, decimal_places=9, blank=True),
        ),
    ]
