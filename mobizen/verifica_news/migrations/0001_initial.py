# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('short_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('fecha', models.DateField()),
                ('image', models.ImageField(upload_to=b'verifica/news/')),
                ('body', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='appentry',
            name='read_more',
            field=models.OneToOneField(related_name='app_entry', to='verifica_news.NewsItem'),
        ),
    ]
