# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-12 16:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drivemee', '0025_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=250, null=True)),
                ('telefono', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[(b'activo', b'Activo'), (b'inactivo', b'Inactivo')], default=b'activo', max_length=20)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proveedor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.AddField(
            model_name='operador',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proveedores', to='drivemee.Proveedor'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitudes', to='drivemee.Proveedor'),
        ),
    ]
