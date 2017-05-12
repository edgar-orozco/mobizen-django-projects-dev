# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0020_auto_20151103_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='SnoozeReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('snoozed_until_date', models.DateTimeField()),
                ('motivo', models.CharField(max_length=200)),
                ('solicitud', models.ForeignKey(related_name='snoozereasons', to='drivemee.Solicitud', null=True)),
            ],
            options={
                'verbose_name_plural': 'Razones',
            },
        ),
    ]
