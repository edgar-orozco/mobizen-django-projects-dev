# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0012_solicitud_costo_real'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='snooze_until_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
