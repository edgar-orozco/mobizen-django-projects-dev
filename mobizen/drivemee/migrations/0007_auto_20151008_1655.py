# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0006_auto_20151007_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operador',
            name='foto',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='operador',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
