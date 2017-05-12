# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0014_auto_20160405_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='programa',
            name='version',
            field=models.SmallIntegerField(default='0'),
            preserve_default=False,
        ),
    ]
