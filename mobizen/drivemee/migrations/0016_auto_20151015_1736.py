# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0015_cupon_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='linked_solicitudes',
            field=models.ForeignKey(related_name='linkeadas', blank=True, to='drivemee.Solicitud', null=True),
        ),
    ]
