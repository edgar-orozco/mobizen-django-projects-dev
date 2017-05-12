# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivemee', '0007_auto_20151008_1655'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operador',
            options={'ordering': ['nombre'], 'verbose_name_plural': 'Operadores'},
        ),
        migrations.RenameField(
            model_name='operador',
            old_name='name',
            new_name='nombre',
        ),
    ]
