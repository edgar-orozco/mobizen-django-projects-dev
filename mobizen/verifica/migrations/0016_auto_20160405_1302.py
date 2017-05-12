# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0015_programa_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reglacirculacion',
            name='semanas',
            field=models.ManyToManyField(to='verifica.Semana', null=True, blank=True),
        ),
    ]
