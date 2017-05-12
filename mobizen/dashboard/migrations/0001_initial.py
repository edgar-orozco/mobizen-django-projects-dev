# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyActiveUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateField(auto_now_add=True, unique=True)),
                ('number_of_users', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DailyTotalUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateField(auto_now_add=True, unique=True)),
                ('number_of_users', models.IntegerField()),
            ],
        ),
    ]
