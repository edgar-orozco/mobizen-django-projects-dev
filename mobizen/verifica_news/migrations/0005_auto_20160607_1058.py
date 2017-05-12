# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica_news', '0004_appentry_important'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsitem',
            name='body',
        ),
        migrations.AddField(
            model_name='appentry',
            name='link',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
