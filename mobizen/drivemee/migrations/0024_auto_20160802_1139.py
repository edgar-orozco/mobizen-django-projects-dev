# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0023_auto_20160428_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='linked_solicitudes',
            field=models.ForeignKey(related_name='linkeadas', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='drivemee.Solicitud', null=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='operador',
            field=models.ForeignKey(related_name='solicitudes', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='drivemee.Operador', null=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='vehiculo',
            field=models.ForeignKey(related_name='solicitudes', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='verifica.Vehiculo', null=True),
        ),
    ]
