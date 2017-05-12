# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0004_auto_20151007_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccion',
            name='solicitud',
            field=models.ForeignKey(related_name='direcciones', to='drivemee.Solicitud'),
        ),
    ]
