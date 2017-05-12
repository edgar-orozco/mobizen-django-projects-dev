# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0005_vehiculo_did_fetch_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenencia',
            name='pagado',
        ),
    ]
