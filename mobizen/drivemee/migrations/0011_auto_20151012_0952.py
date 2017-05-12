# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0010_operador_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='operador',
            name='email',
            field=models.EmailField(default='none@mail.com', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operador',
            name='telefono',
            field=models.CharField(default='5512345678', max_length=20),
            preserve_default=False,
        ),
    ]
