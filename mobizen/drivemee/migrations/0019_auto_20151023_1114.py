# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0018_solicitud_sent_reminder_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='status',
            field=models.CharField(default=b'abierto', max_length=20, choices=[(b'abierto', b'Abierto'), (b'agendado', b'Agendado'), (b'proceso', b'En Proceso'), (b'verificado', b'Verificado'), (b'cerrado', b'Concluido'), (b'caido', b'Cita Ca\xc3\xadda'), (b'cancelado', b'Cancelado'), (b'no_contratado', b'No Contratado'), (b'reagendado', b'Reagendado'), (b'pendiente', b'Pendiente'), (b'abandonada', b'Abandonada')]),
        ),
    ]
