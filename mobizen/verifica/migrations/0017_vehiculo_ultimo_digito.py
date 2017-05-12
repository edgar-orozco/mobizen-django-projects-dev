# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0016_auto_20160405_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculo',
            name='ultimo_digito',
            field=models.CharField(max_length=1, blank=True),
        ),
    ]
