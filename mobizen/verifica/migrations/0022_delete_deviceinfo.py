# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0021_remove_client_device_info'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeviceInfo',
        ),
    ]
