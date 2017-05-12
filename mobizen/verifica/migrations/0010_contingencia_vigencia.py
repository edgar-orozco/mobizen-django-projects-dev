# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0009_auto_20160331_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='contingencia',
            name='vigencia',
            field=models.DateField(default=datetime.datetime(2016, 4, 5, 17, 2, 32, 910211, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
