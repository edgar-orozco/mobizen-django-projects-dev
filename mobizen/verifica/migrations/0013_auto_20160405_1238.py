# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0012_auto_20160405_1218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dia',
            options={'ordering': ['-value']},
        ),
        migrations.AlterModelOptions(
            name='holograma',
            options={'ordering': ['-value']},
        ),
        migrations.AlterModelOptions(
            name='semana',
            options={'ordering': ['-value']},
        ),
        migrations.AlterModelOptions(
            name='terminacion',
            options={'ordering': ['-value']},
        ),
    ]
