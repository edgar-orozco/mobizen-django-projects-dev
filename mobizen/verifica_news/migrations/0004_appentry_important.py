# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica_news', '0003_auto_20160602_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='appentry',
            name='important',
            field=models.BooleanField(default=False),
        ),
    ]
