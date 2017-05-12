# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0019_auto_20151023_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operador',
            name='email',
            field=models.EmailField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='snooze_until_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
