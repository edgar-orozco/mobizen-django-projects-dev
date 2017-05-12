# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0014_auto_20151015_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='cupon',
            name='name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
