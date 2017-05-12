# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0018_auto_20160407_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='device_os',
            field=models.CharField(default=None, max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='device_type',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='onesignal_token',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='parse_token',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='push_token',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
    ]
