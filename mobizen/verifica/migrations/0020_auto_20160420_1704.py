# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0019_auto_20160420_1611'),
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
            ],
        ),
        migrations.RemoveField(
            model_name='client',
            name='device_os',
        ),
        migrations.RemoveField(
            model_name='client',
            name='device_type',
        ),
        migrations.RemoveField(
            model_name='client',
            name='onesignal_token',
        ),
        migrations.RemoveField(
            model_name='client',
            name='parse_token',
        ),
        migrations.RemoveField(
            model_name='client',
            name='push_token',
        ),
        migrations.AddField(
            model_name='client',
            name='device_info',
            field=models.ForeignKey(blank=True, to='verifica.DeviceInfo', null=True),
        ),
    ]
