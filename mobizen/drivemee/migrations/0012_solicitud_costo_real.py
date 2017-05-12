# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0011_auto_20151012_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='costo_real',
            field=models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2, blank=True),
        ),
    ]
