# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifica', '0007_auto_20160330_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contingencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.SmallIntegerField(unique=True)),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Dia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.SmallIntegerField(unique=True)),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Holograma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(unique=True, max_length=10, choices=[(b'DOBLE CERO', b'Doble Cero'), (b'CERO', b'Cero'), (b'UNO', b'Uno'), (b'DOS', b'Dos'), (b'EXENTO', b'Exento')])),
            ],
        ),
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vigencia_inicio', models.DateField()),
                ('vigencia_fin', models.DateField()),
                ('title', models.CharField(max_length=20)),
                ('dias', models.ManyToManyField(to='verifica.Dia')),
            ],
        ),
        migrations.CreateModel(
            name='ReglaCirculacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('hologramas', models.ManyToManyField(to='verifica.Holograma')),
            ],
        ),
        migrations.CreateModel(
            name='Semana',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.SmallIntegerField(unique=True)),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Terminacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(unique=True, max_length=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='regla',
            name='placa',
        ),
        migrations.DeleteModel(
            name='ReglaEntidad',
        ),
        migrations.DeleteModel(
            name='Regla',
        ),
        migrations.AddField(
            model_name='reglacirculacion',
            name='semanas',
            field=models.ManyToManyField(to='verifica.Semana', null=True),
        ),
        migrations.AddField(
            model_name='reglacirculacion',
            name='terminaciones',
            field=models.ManyToManyField(to='verifica.Terminacion'),
        ),
        migrations.AddField(
            model_name='dia',
            name='reglas',
            field=models.ManyToManyField(to='verifica.ReglaCirculacion'),
        ),
        migrations.AddField(
            model_name='contingencia',
            name='reglas',
            field=models.ManyToManyField(to='verifica.ReglaCirculacion'),
        ),
    ]
