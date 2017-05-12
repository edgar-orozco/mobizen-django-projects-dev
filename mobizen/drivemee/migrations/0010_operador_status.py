# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0009_auto_20151008_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='operador',
            name='status',
            field=models.CharField(default=b'activo', max_length=20, choices=[(b'activo', b'Activo'), (b'inactivo', b'Inactivo')]),
        ),
    ]
