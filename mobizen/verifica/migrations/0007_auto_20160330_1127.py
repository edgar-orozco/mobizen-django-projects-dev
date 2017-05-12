# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0006_remove_tenencia_pagado'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imeca',
            options={'ordering': ['-pk', '-fecha']},
        ),
    ]
