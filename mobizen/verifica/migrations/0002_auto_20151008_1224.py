# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import localflavor.mx.models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoPlaca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=20, choices=[(b'Particular', b'Particular'), (b'Discapacitado', b'Discapacitado'), (b'Motocicleta', b'Motocicleta'), (b'Taxi', b'Taxi')])),
                ('estado', localflavor.mx.models.MXStateField(max_length=3, null=True, choices=[('AGU', 'Aguascalientes'), ('BCN', 'Baja California'), ('BCS', 'Baja California Sur'), ('CAM', 'Campeche'), ('CHH', 'Chihuahua'), ('CHP', 'Chiapas'), ('COA', 'Coahuila'), ('COL', 'Colima'), ('DIF', 'Distrito Federal'), ('DUR', 'Durango'), ('GRO', 'Guerrero'), ('GUA', 'Guanajuato'), ('HID', 'Hidalgo'), ('JAL', 'Jalisco'), ('MEX', 'Estado de M\xe9xico'), ('MIC', 'Michoac\xe1n'), ('MOR', 'Morelos'), ('NAY', 'Nayarit'), ('NLE', 'Nuevo Le\xf3n'), ('OAX', 'Oaxaca'), ('PUE', 'Puebla'), ('QUE', 'Quer\xe9taro'), ('ROO', 'Quintana Roo'), ('SIN', 'Sinaloa'), ('SLP', 'San Luis Potos\xed'), ('SON', 'Sonora'), ('TAB', 'Tabasco'), ('TAM', 'Tamaulipas'), ('TLA', 'Tlaxcala'), ('VER', 'Veracruz'), ('YUC', 'Yucat\xe1n'), ('ZAC', 'Zacatecas')])),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='placa',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='placa',
            name='entidad',
        ),
        migrations.AlterField(
            model_name='regla',
            name='placa',
            field=models.OneToOneField(to='verifica.TipoPlaca'),
        ),
        migrations.DeleteModel(
            name='Entidad',
        ),
        migrations.DeleteModel(
            name='Placa',
        ),
        migrations.AlterUniqueTogether(
            name='tipoplaca',
            unique_together=set([('estado', 'tipo')]),
        ),
    ]
