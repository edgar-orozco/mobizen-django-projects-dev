# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0013_solicitud_snooze_until_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='linked_solicitudes',
            field=models.ForeignKey(blank=True, to='drivemee.Solicitud', null=True),
        ),
        migrations.AlterField(
            model_name='calificacioncliente',
            name='solicitud',
            field=models.OneToOneField(related_name='calificacion', to='drivemee.Solicitud'),
        ),
    ]
