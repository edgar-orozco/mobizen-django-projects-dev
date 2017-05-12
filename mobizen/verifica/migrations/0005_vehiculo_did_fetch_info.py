# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0004_tenencia_pagado'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculo',
            name='did_fetch_info',
            field=models.BooleanField(default=False),
        ),
    ]
