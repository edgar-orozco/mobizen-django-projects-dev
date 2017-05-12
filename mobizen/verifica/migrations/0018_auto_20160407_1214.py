# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0017_vehiculo_ultimo_digito'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='programa',
            options={'ordering': ['version'], 'get_latest_by': 'timestamp'},
        ),
        migrations.AddField(
            model_name='programa',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 7, 17, 14, 35, 798953, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
