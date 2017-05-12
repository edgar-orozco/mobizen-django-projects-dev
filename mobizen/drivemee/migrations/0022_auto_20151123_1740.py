# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0021_snoozereason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacion',
            name='comentarios',
            field=models.CharField(max_length=2500, null=True, blank=True),
        ),
    ]
