# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0008_auto_20151008_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operador',
            name='calificacion',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=2, blank=True),
        ),
    ]
