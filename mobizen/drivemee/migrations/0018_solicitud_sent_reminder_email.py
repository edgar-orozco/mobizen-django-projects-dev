# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0017_auto_20151022_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='sent_reminder_email',
            field=models.BooleanField(default=False),
        ),
    ]
