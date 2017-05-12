# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import localflavor.mx.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alertas_hnc', models.BooleanField(default=True)),
                ('alertas_mnc', models.BooleanField(default=True)),
                ('hora_alertas_verificacion', models.CommaSeparatedIntegerField(default=b'10,30', max_length=5)),
                ('hora_alertas_hnc', models.CommaSeparatedIntegerField(default=b'5,00', max_length=5)),
                ('hora_alertas_mnc', models.CommaSeparatedIntegerField(default=b'22,00', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='AppVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=10, blank=True)),
                ('title', models.CharField(max_length=30, blank=True)),
            ],
            options={
                'ordering': ['-version'],
                'get_latest_by': 'version',
            },
        ),
        migrations.CreateModel(
            name='Aseguradora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BuildNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('body', models.CharField(max_length=255, blank=True)),
                ('button', models.CharField(max_length=50)),
                ('actionTarget', models.CharField(max_length=255, blank=True)),
                ('actionType', models.CharField(default=b'dismiss', max_length=20, choices=[(b'dismiss', b'Dismiss View'), (b'url', b'Open Link'), (b'none', b'No Action')])),
            ],
        ),
        migrations.CreateModel(
            name='Builds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(unique=True)),
                ('isDebug', models.BooleanField(default=False)),
                ('version', models.ForeignKey(related_name='builds', to='verifica.AppVersion')),
            ],
            options={
                'ordering': ['number'],
                'get_latest_by': 'number',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('deviceToken', models.CharField(max_length=16, unique=True, serialize=False, primary_key=True, db_index=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(default=None, null=True, blank=True)),
                ('appVersion', models.ForeignKey(blank=True, to='verifica.AppVersion', null=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Comparacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('fecha', models.DateField()),
                ('coche_registrado', models.BooleanField(default=True)),
                ('id_auto', models.CharField(max_length=10, null=True, blank=True)),
                ('codigo_colonia', models.CharField(max_length=10, null=True, blank=True)),
                ('codigo_postal', models.CharField(max_length=6, null=True, blank=True)),
                ('elapsed', models.DecimalField(default=0.0, max_digits=5, decimal_places=3)),
                ('timeout', models.BooleanField(default=False)),
                ('error_message', models.CharField(max_length=250, null=True, blank=True)),
                ('nombre', models.CharField(max_length=100, null=True, blank=True)),
                ('email', models.CharField(max_length=250, null=True, blank=True)),
                ('telefono', models.CharField(max_length=20, null=True, blank=True)),
                ('descripcion', models.CharField(max_length=250, null=True, blank=True)),
                ('client', models.ForeignKey(related_name='comparaciones', blank=True, to='verifica.Client', null=True)),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name_plural': 'Comparaciones',
            },
        ),
        migrations.CreateModel(
            name='Costo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('costo', models.CharField(default=b'0', max_length=10)),
                ('aseguradora', models.ForeignKey(blank=True, to='verifica.Aseguradora', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('deviceToken', models.CharField(max_length=16, unique=True, serialize=False, primary_key=True, db_index=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('fecha', models.DateField()),
                ('costo', models.CharField(default=b'0', max_length=10)),
                ('coche_registrado', models.BooleanField(default=True)),
                ('aseguradora', models.ForeignKey(blank=True, to='verifica.Aseguradora', null=True)),
                ('client', models.ForeignKey(related_name='cotizaciones', to='verifica.Client')),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name_plural': 'Cotizaciones',
            },
        ),
        migrations.CreateModel(
            name='CotizadorError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(default=True, max_length=255)),
                ('cotizacion', models.ForeignKey(related_name='errores', to='verifica.Cotizacion')),
            ],
        ),
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Feriado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Imeca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imecas', models.CharField(max_length=4)),
                ('particula', models.CharField(max_length=15)),
                ('indice_uv', models.CharField(max_length=4, null=True, blank=True)),
                ('hora', models.CharField(default=b'0', max_length=2)),
                ('fecha', models.DateField()),
            ],
            options={
                'ordering': ['fecha'],
            },
        ),
        migrations.CreateModel(
            name='Infraccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('folio', models.CharField(max_length=50)),
                ('fecha', models.DateField()),
                ('situacion', models.CharField(default=b'NO', max_length=30, choices=[(b'Pagada', b'Pagada'), (b'No Pagada', b'No Pagada')])),
                ('motivo', models.CharField(max_length=300)),
                ('fundamento', models.CharField(max_length=255)),
                ('short_fundamento', models.CharField(max_length=50, null=True, blank=True)),
                ('sancion', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=100)),
                ('valor_interesse', models.SmallIntegerField(unique=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['valor_interesse'],
            },
        ),
        migrations.CreateModel(
            name='Placa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=20, choices=[(b'Particular', b'Particular'), (b'Discapacitado', b'Discapacitado'), (b'Motocicleta', b'Motocicleta'), (b'Taxi', b'Taxi')])),
                ('entidad', models.ForeignKey(related_name='placas', to='verifica.Entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Plazo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=100)),
                ('valor_interesse', models.SmallIntegerField(unique=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['valor_interesse'],
            },
        ),
        migrations.CreateModel(
            name='Recibo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poliza', models.CharField(max_length=100)),
                ('cancelado', models.BooleanField(default=False)),
                ('cotizacion', models.ForeignKey(related_name='recibos', to='verifica.Cotizacion')),
            ],
        ),
        migrations.CreateModel(
            name='Regla',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hoy_no_circula', models.BooleanField(default=False)),
                ('hoy_no_circula_sabatino', models.BooleanField(default=False)),
                ('verificacion', models.BooleanField(default=False)),
                ('placa', models.OneToOneField(to='verifica.Placa')),
            ],
        ),
        migrations.CreateModel(
            name='ReglaEntidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hoy_no_circula_sabatino', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ReleaseNotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('body', models.CharField(max_length=255, blank=True)),
                ('button', models.CharField(max_length=50)),
                ('actionTarget', models.CharField(max_length=255, blank=True)),
                ('actionType', models.CharField(default=b'dismiss', max_length=20, choices=[(b'dismiss', b'Dismiss View'), (b'url', b'Open Link'), (b'none', b'No Action')])),
                ('version', models.ForeignKey(related_name='notas', to='verifica.AppVersion')),
            ],
        ),
        migrations.CreateModel(
            name='SalarioMinimo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(unique=True, max_length=4)),
                ('valor', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Seguro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poliza', models.CharField(max_length=30, null=True, blank=True)),
                ('titular', models.CharField(max_length=100, null=True, blank=True)),
                ('vigencia', models.DateField(null=True)),
                ('activo', models.BooleanField(default=True)),
                ('boughtInApp', models.BooleanField(default=False)),
                ('aseguradora', models.ForeignKey(blank=True, to='verifica.Aseguradora', null=True)),
                ('cobertura', models.ForeignKey(blank=True, to='verifica.Paquete', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado', localflavor.mx.models.MXStateField(max_length=3, choices=[('AGU', 'Aguascalientes'), ('BCN', 'Baja California'), ('BCS', 'Baja California Sur'), ('CAM', 'Campeche'), ('CHH', 'Chihuahua'), ('CHP', 'Chiapas'), ('COA', 'Coahuila'), ('COL', 'Colima'), ('DIF', 'Distrito Federal'), ('DUR', 'Durango'), ('GRO', 'Guerrero'), ('GUA', 'Guanajuato'), ('HID', 'Hidalgo'), ('JAL', 'Jalisco'), ('MEX', 'Estado de M\xe9xico'), ('MIC', 'Michoac\xe1n'), ('MOR', 'Morelos'), ('NAY', 'Nayarit'), ('NLE', 'Nuevo Le\xf3n'), ('OAX', 'Oaxaca'), ('PUE', 'Puebla'), ('QUE', 'Quer\xe9taro'), ('ROO', 'Quintana Roo'), ('SIN', 'Sinaloa'), ('SLP', 'San Luis Potos\xed'), ('SON', 'Sonora'), ('TAB', 'Tabasco'), ('TAM', 'Tamaulipas'), ('TLA', 'Tlaxcala'), ('VER', 'Veracruz'), ('YUC', 'Yucat\xe1n'), ('ZAC', 'Zacatecas')])),
                ('footer', models.CharField(max_length=250, null=True, blank=True)),
                ('salario_minimo', models.ForeignKey(to='verifica.SalarioMinimo')),
            ],
            options={
                'ordering': ['estado'],
            },
        ),
        migrations.CreateModel(
            name='TarifaItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.SmallIntegerField()),
                ('name', models.CharField(default=True, max_length=255)),
                ('costo', models.CharField(default=True, max_length=12)),
                ('tarifa', models.ForeignKey(related_name='items', to='verifica.Tarifa')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Telefono',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30, null=True, blank=True)),
                ('telnumber', models.CharField(max_length=30, null=True, blank=True)),
                ('aseguradora', models.ForeignKey(related_name='telefonos', to='verifica.Aseguradora')),
            ],
        ),
        migrations.CreateModel(
            name='Tenencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('periodo', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=50, null=True)),
                ('placa', models.CharField(max_length=30, blank=True)),
                ('modelo', models.SmallIntegerField(null=True, blank=True)),
                ('vin', models.CharField(max_length=20, blank=True)),
                ('tarjeta_circulacion_permanente', models.BooleanField(default=False)),
                ('tarjeta_circulacion_vigencia', models.DateField(null=True, blank=True)),
                ('codigo_postal', models.CharField(max_length=5, blank=True)),
                ('query_string', models.CharField(max_length=100, blank=True)),
                ('exento', models.BooleanField(default=False)),
                ('es_par', models.BooleanField(default=False)),
                ('dia_no_circula', models.SmallIntegerField(default=5)),
                ('custom_modelo', models.BooleanField(default=False)),
                ('custom_car', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(blank=True, to='verifica.Car', null=True)),
                ('client', models.ForeignKey(related_name='vehiculos', to='verifica.Client')),
            ],
        ),
        migrations.CreateModel(
            name='VehiculoConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alerta_inicio', models.BooleanField(default=True)),
                ('alerta_mes', models.BooleanField(default=True)),
                ('alerta_quincena', models.BooleanField(default=True)),
                ('alerta_semana', models.BooleanField(default=True)),
                ('alerta_fin', models.BooleanField(default=True)),
                ('vehiculo', models.ForeignKey(related_name='config', to='verifica.Vehiculo', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Verificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resultado', models.CharField(max_length=10, blank=True)),
                ('fecha', models.DateField(null=True, blank=True)),
                ('vigencia', models.DateField(null=True, blank=True)),
                ('manual', models.BooleanField(default=False)),
                ('vehiculo', models.ForeignKey(related_name='verificacion', to='verifica.Vehiculo', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='tenencia',
            name='vehiculo',
            field=models.ForeignKey(related_name='tenencias', to='verifica.Vehiculo'),
        ),
        migrations.AddField(
            model_name='seguro',
            name='vehiculo',
            field=models.ForeignKey(related_name='seguro', null=True, to='verifica.Vehiculo', unique=True),
        ),
        migrations.AddField(
            model_name='recibo',
            name='seguro',
            field=models.ForeignKey(related_name='recibo', blank=True, to='verifica.Seguro', null=True),
        ),
        migrations.AddField(
            model_name='recibo',
            name='vehiculo',
            field=models.ForeignKey(related_name='recibo', blank=True, to='verifica.Vehiculo', null=True),
        ),
        migrations.AddField(
            model_name='infraccion',
            name='vehiculo',
            field=models.ForeignKey(related_name='infracciones', to='verifica.Vehiculo'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='paquete',
            field=models.ForeignKey(related_name='recibos', to='verifica.Paquete'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='plazo',
            field=models.ForeignKey(related_name='recibos', to='verifica.Plazo'),
        ),
        migrations.AddField(
            model_name='comparacion',
            name='costos',
            field=models.ManyToManyField(to='verifica.Costo', null=True),
        ),
        migrations.AddField(
            model_name='comparacion',
            name='paquete',
            field=models.ForeignKey(to='verifica.Paquete'),
        ),
        migrations.AddField(
            model_name='comparacion',
            name='plazo',
            field=models.ForeignKey(to='verifica.Plazo'),
        ),
        migrations.AddField(
            model_name='car',
            name='manufacturer',
            field=models.ForeignKey(to='verifica.Manufacturer'),
        ),
        migrations.AddField(
            model_name='buildnote',
            name='build',
            field=models.ForeignKey(related_name='notas', to='verifica.Builds'),
        ),
        migrations.AddField(
            model_name='appconfig',
            name='client',
            field=models.OneToOneField(related_name='config', to='verifica.Client'),
        ),
        migrations.AlterUniqueTogether(
            name='vehiculo',
            unique_together=set([('client', 'placa')]),
        ),
        migrations.AlterUniqueTogether(
            name='tenencia',
            unique_together=set([('vehiculo', 'periodo')]),
        ),
        migrations.AlterUniqueTogether(
            name='telefono',
            unique_together=set([('aseguradora', 'telnumber')]),
        ),
        migrations.AlterUniqueTogether(
            name='tarifaitem',
            unique_together=set([('tarifa', 'order')]),
        ),
        migrations.AlterUniqueTogether(
            name='placa',
            unique_together=set([('entidad', 'tipo')]),
        ),
        migrations.AlterUniqueTogether(
            name='infraccion',
            unique_together=set([('vehiculo', 'folio')]),
        ),
    ]
