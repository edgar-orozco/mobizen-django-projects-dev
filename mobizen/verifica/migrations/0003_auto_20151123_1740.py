# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0002_auto_20151008_1224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paquete',
            options={'ordering': ['internal_order']},
        ),
        migrations.AddField(
            model_name='paquete',
            name='internal_order',
            field=models.SmallIntegerField(unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='car',
            unique_together=set([('name', 'manufacturer')]),
        ),
    ]
