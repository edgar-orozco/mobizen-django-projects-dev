# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0023_deviceinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='infraccion',
            name='forced_pago',
            field=models.BooleanField(default=False),
        ),
    ]
