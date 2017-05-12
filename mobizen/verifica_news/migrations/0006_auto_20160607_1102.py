# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('verifica_news', '0005_auto_20160607_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appentry',
            name='read_more',
        ),
        migrations.AddField(
            model_name='appentry',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 6, 7, 16, 2, 17, 634668, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appentry',
            name='image',
            field=models.ImageField(null=True, upload_to=b'verifica/news/', blank=True),
        ),
        migrations.AddField(
            model_name='appentry',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 7, 16, 2, 21, 335026, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='NewsItem',
        ),
    ]
