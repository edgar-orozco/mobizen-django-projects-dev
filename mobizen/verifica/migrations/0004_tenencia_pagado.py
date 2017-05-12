# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0003_auto_20151123_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenencia',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
    ]
