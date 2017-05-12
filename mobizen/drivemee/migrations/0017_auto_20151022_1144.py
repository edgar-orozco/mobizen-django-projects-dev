# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0016_auto_20151015_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='timestamp_confirmacion',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='status',
            field=models.CharField(default=b'abierto', max_length=20, choices=[(b'abierto', b'Abierto'), (b'agendado', b'Agendado'), (b'proceso', b'En Proceso'), (b'verificado', b'Verificado'), (b'cerrado', b'Concluido'), (b'caido', b'Cita Ca\xc3\xadda'), (b'cancelado', b'Cancelado'), (b'no_contratado', b'No Contratado'), (b'reagendado', b'Reagendado'), (b'pendiente', b'Pendiente')]),
        ),
    ]
