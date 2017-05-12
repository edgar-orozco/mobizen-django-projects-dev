# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0020_auto_20160420_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='device_info',
        ),
    ]
