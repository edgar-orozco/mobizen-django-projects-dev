# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-15 21:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0025_client_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='user',
        ),
    ]
