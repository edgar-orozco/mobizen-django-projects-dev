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
            name='CalificacionCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('calificacion', models.DecimalField(max_digits=3, decimal_places=2, blank=True)),
                ('motivo', models.CharField(max_length=250)),
                ('client', models.ForeignKey(related_name='calificaciones', to='verifica.Client')),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name_plural': 'Calificaciones',
            },
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Cupon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('codigo', models.CharField(unique=True, max_length=15)),
                ('vigencia', models.DateTimeField(null=True, blank=True)),
                ('activo', models.BooleanField(default=True)),
                ('permanente', models.BooleanField(default=True)),
                ('descuento', models.IntegerField()),
                ('numero_usos', models.IntegerField(default=0)),
                ('tipo', models.CharField(default=b'valet', max_length=20, choices=[(b'valet', b'Servicio de Valet'), (b'verificentro', b'Verificentro')])),
                ('client', models.ForeignKey(related_name='cupones', blank=True, to='verifica.Client', null=True)),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name_plural': 'Cupones',
            },
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calle', models.CharField(max_length=200)),
                ('numero_exterior', models.CharField(max_length=100, null=True, blank=True)),
                ('numero_interior', models.CharField(max_length=100, null=True, blank=True)),
                ('colonia', models.CharField(max_length=100, null=True, blank=True)),
                ('municipio', models.CharField(max_length=100, null=True, blank=True)),
                ('estado', localflavor.mx.models.MXStateField(max_length=3, choices=[('AGU', 'Aguascalientes'), ('BCN', 'Baja California'), ('BCS', 'Baja California Sur'), ('CAM', 'Campeche'), ('CHH', 'Chihuahua'), ('CHP', 'Chiapas'), ('COA', 'Coahuila'), ('COL', 'Colima'), ('DIF', 'Distrito Federal'), ('DUR', 'Durango'), ('GRO', 'Guerrero'), ('GUA', 'Guanajuato'), ('HID', 'Hidalgo'), ('JAL', 'Jalisco'), ('MEX', 'Estado de M\xe9xico'), ('MIC', 'Michoac\xe1n'), ('MOR', 'Morelos'), ('NAY', 'Nayarit'), ('NLE', 'Nuevo Le\xf3n'), ('OAX', 'Oaxaca'), ('PUE', 'Puebla'), ('QUE', 'Quer\xe9taro'), ('ROO', 'Quintana Roo'), ('SIN', 'Sinaloa'), ('SLP', 'San Luis Potos\xed'), ('SON', 'Sonora'), ('TAB', 'Tabasco'), ('TAM', 'Tamaulipas'), ('TLA', 'Tlaxcala'), ('VER', 'Veracruz'), ('YUC', 'Yucat\xe1n'), ('ZAC', 'Zacatecas')])),
                ('codigo_postal', localflavor.mx.models.MXZipCodeField(max_length=5, null=True, blank=True)),
                ('latitud', models.DecimalField(null=True, max_digits=20, decimal_places=15, blank=True)),
                ('longitud', models.DecimalField(null=True, max_digits=20, decimal_places=15, blank=True)),
                ('referencias', models.CharField(max_length=200, null=True, blank=True)),
                ('tipo', models.CharField(max_length=11, choices=[(b'recoleccion', b'Recolecci\xc3\xb3n'), (b'entrega', b'Entrega'), (b'ambos', b'Ambos')])),
            ],
            options={
                'verbose_name_plural': 'Direcciones',
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adeudos', models.BooleanField(default=False)),
                ('seguro', models.BooleanField(default=False)),
                ('certificado', models.BooleanField(default=False)),
                ('tarjeta', models.BooleanField(default=False)),
                ('enterado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('comentarios', models.CharField(max_length=250, null=True, blank=True)),
                ('calificacion', models.DecimalField(null=True, max_digits=3, decimal_places=2, blank=True)),
                ('no_quiso_calificar', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name_plural': 'Evaluaciones',
            },
        ),
        migrations.CreateModel(
            name='Operador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('foto', models.CharField(max_length=50)),
                ('calificacion', models.DecimalField(max_digits=3, decimal_places=2, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Operadores',
            },
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('motivo', models.CharField(max_length=250)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('resultado', models.CharField(default=b'CERO', max_length=10, choices=[(b'DOBLE CERO', b'Doble Cero'), (b'CERO', b'Cero'), (b'UNO', b'Uno'), (b'DOS', b'Dos'), (b'RECHAZO', b'Rechazo')])),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('folio', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp_abierto', models.DateTimeField(auto_now_add=True)),
                ('timestamp_cerrado', models.DateTimeField(null=True, blank=True)),
                ('timestamp_agendado', models.DateTimeField(null=True, blank=True)),
                ('timestamp_proceso', models.DateTimeField(null=True, blank=True)),
                ('nombre', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=250)),
                ('telefono', models.CharField(max_length=20)),
                ('placa', models.CharField(max_length=20)),
                ('marca', models.CharField(max_length=20)),
                ('submarca', models.CharField(max_length=20)),
                ('modelo', models.SmallIntegerField()),
                ('ultimo_holograma', models.CharField(default=b'', max_length=20, null=True, blank=True)),
                ('coche_registrado', models.BooleanField(default=True)),
                ('status', models.CharField(default=b'abierto', max_length=20, choices=[(b'abierto', b'Abierto'), (b'agendado', b'Agendado'), (b'proceso', b'En Proceso'), (b'verificado', b'Verificado'), (b'cerrado', b'Concluido'), (b'caido', b'Cita Ca\xc3\xadda'), (b'cancelado', b'Cancelado'), (b'no_contratado', b'No Contratado'), (b'reagendado', b'Reagendado')])),
                ('client', models.ForeignKey(related_name='solicitudes', to='verifica.Client')),
                ('cupon', models.ForeignKey(blank=True, to='drivemee.Cupon', null=True)),
                ('operador', models.ForeignKey(related_name='solicitudes', blank=True, to='drivemee.Operador', null=True)),
            ],
            options={
                'ordering': ['-timestamp_abierto'],
                'verbose_name_plural': 'Solicitudes',
            },
        ),
        migrations.CreateModel(
            name='SolicitudInternal',
            fields=[
                ('deviceToken', models.CharField(max_length=16, unique=True, serialize=False, primary_key=True, db_index=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(default=b'normal', max_length=20, choices=[(b'normal', b'Tarifa Normal'), (b'tarde', b'Tarifa \xc3\x9altima Semana')])),
                ('estado', localflavor.mx.models.MXStateField(max_length=3, choices=[('AGU', 'Aguascalientes'), ('BCN', 'Baja California'), ('BCS', 'Baja California Sur'), ('CAM', 'Campeche'), ('CHH', 'Chihuahua'), ('CHP', 'Chiapas'), ('COA', 'Coahuila'), ('COL', 'Colima'), ('DIF', 'Distrito Federal'), ('DUR', 'Durango'), ('GRO', 'Guerrero'), ('GUA', 'Guanajuato'), ('HID', 'Hidalgo'), ('JAL', 'Jalisco'), ('MEX', 'Estado de M\xe9xico'), ('MIC', 'Michoac\xe1n'), ('MOR', 'Morelos'), ('NAY', 'Nayarit'), ('NLE', 'Nuevo Le\xf3n'), ('OAX', 'Oaxaca'), ('PUE', 'Puebla'), ('QUE', 'Quer\xe9taro'), ('ROO', 'Quintana Roo'), ('SIN', 'Sinaloa'), ('SLP', 'San Luis Potos\xed'), ('SON', 'Sonora'), ('TAB', 'Tabasco'), ('TAM', 'Tamaulipas'), ('TLA', 'Tlaxcala'), ('VER', 'Veracruz'), ('YUC', 'Yucat\xe1n'), ('ZAC', 'Zacatecas')])),
                ('costo', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
            ],
            options={
                'ordering': ['estado'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='tarifa',
            unique_together=set([('tipo', 'estado')]),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='solicitudToken',
            field=models.OneToOneField(null=True, blank=True, to='drivemee.SolicitudInternal'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='vehiculo',
            field=models.ForeignKey(related_name='solicitudes', blank=True, to='verifica.Vehiculo', null=True),
        ),
        migrations.AddField(
            model_name='resultado',
            name='solicitud',
            field=models.OneToOneField(related_name='resultado', to='drivemee.Solicitud'),
        ),
        migrations.AddField(
            model_name='reporte',
            name='solicitud',
            field=models.OneToOneField(related_name='reporte', to='drivemee.Solicitud'),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='operador',
            field=models.ForeignKey(related_name='evaluaciones', blank=True, to='drivemee.Operador', null=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='solicitud',
            field=models.OneToOneField(related_name='evaluacion', to='drivemee.Solicitud'),
        ),
        migrations.AddField(
            model_name='documento',
            name='solicitud',
            field=models.OneToOneField(related_name='documentos', to='drivemee.Solicitud'),
        ),
        migrations.AddField(
            model_name='direccion',
            name='solicitud',
            field=models.ForeignKey(related_name='direcciones', to='drivemee.Solicitud'),
        ),
        migrations.AddField(
            model_name='cupon',
            name='empresa',
            field=models.ForeignKey(related_name='cupones', blank=True, to='drivemee.Empresa', null=True),
        ),
        migrations.AddField(
            model_name='cita',
            name='solicitud',
            field=models.OneToOneField(related_name='cita', to='drivemee.Solicitud'),
        ),
        migrations.AddField(
            model_name='calificacioncliente',
            name='solicitud',
            field=models.OneToOneField(related_name='solicitud', to='drivemee.Solicitud'),
        ),
    ]
