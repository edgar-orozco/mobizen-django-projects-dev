# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0022_delete_deviceinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('onesignal_token', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('parse_token', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('push_token', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('device_type', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('device_os', models.CharField(default=None, max_length=10, null=True, blank=True)),
                ('device_os_version', models.CharField(default=None, max_length=10, null=True, blank=True)),
                ('client', models.OneToOneField(related_name='device', to='verifica.Client')),
            ],
        ),
    ]
