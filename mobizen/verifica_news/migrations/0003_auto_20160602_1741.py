# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica_news', '0002_auto_20160526_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='appentry',
            name='platform_android',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='appentry',
            name='platform_ios',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='appentry',
            name='short_description',
            field=models.TextField(max_length=255),
        ),
    ]
