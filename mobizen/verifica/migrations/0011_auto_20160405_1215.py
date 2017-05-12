# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0010_contingencia_vigencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='dia',
            name='day_name',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AlterField(
            model_name='dia',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
