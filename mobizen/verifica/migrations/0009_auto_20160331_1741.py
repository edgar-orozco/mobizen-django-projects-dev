# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0008_auto_20160331_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contingencia',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='programa',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='reglacirculacion',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
