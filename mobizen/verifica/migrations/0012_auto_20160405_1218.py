# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0011_auto_20160405_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contingencia',
            name='value',
        ),
        migrations.AlterField(
            model_name='dia',
            name='value',
            field=models.SmallIntegerField(),
        ),
    ]
