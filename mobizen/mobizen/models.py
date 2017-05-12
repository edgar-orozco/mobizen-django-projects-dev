# -*- coding: utf-8 -*- 
import datetime
import string
import unicodedata
from django.utils import timezone
from django.db import models
from django.db.models import signals
from django.core.urlresolvers import reverse
from localflavor.mx.models import MXStateField, MXZipCodeField
from verifica.random_primary import RandomPrimaryIdModel
from verifica.models import Client, Vehiculo

class Tarifa(models.Model):
    TARIFA_CHOICES = (
        ('normal', 'Tarifa Normal'),
        ('tarde', 'Tarifa Última Semana'),
    )
    tipo = models.CharField(max_length=20, choices=TARIFA_CHOICES, default='normal')
    estado = MXStateField()
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def __unicode__(self):
        return unicode(self.estado + ' ' + self.tipo)
    class Meta:
        ordering = ['estado']
        unique_together = (("tipo", "estado"),)

class Empresa(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __unicode__(self):
        return unicode(self.name)
    class Meta:
        ordering = ['name']

class Cupon(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=15, unique=True, blank=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    vigencia = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    permanente = models.BooleanField(default=True)
    descuento = models.IntegerField(blank=False)
    numero_usos = models.IntegerField(blank=False, default=0)
    empresa = models.ForeignKey(Empresa, related_name='cupones', blank=True, null=True)
    client = models.ForeignKey(Client, related_name='cupones', blank=True, null=True)
    CUPON_CHOICES = (
        ('valet', 'Servicio de Valet'),
        ('verificentro', 'Verificentro'),
    )
    tipo = models.CharField(max_length=20, choices=CUPON_CHOICES, default='valet')
    def __unicode__(self):
        return unicode(self.codigo)
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Cupones'

class Operador(models.Model):
    nombre = models.CharField(max_length=50)
    foto = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    telefono = models.CharField(max_length=20)
    calificacion = models.DecimalField(blank=True, max_digits=3, decimal_places=2, null=True)
    OP_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    status = models.CharField(max_length=20, choices=OP_CHOICES, default='activo')
    def __unicode__(self):
        return unicode(self.nombre)
    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Operadores'

class SolicitudInternal(RandomPrimaryIdModel):
    timestamp = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return unicode(self.deviceToken)

class Solicitud(models.Model):
    solicitudToken = models.OneToOneField(SolicitudInternal, blank=True, null=True)
    client = models.ForeignKey(Client, related_name='solicitudes')
    vehiculo = models.ForeignKey(Vehiculo, related_name='solicitudes', blank=True, null=True, on_delete=models.SET_NULL)
    folio = models.AutoField(primary_key=True)
    timestamp_abierto = models.DateTimeField(auto_now_add=True)
    timestamp_cerrado = models.DateTimeField(blank=True, null=True)
    timestamp_agendado = models.DateTimeField(blank=True, null=True)
    timestamp_proceso = models.DateTimeField(blank=True, null=True)
    timestamp_confirmacion = models.DateTimeField(blank=True, null=True)
    snooze_until_date = models.DateTimeField(blank=True, null=True)
    costo_real = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=250)
    telefono = models.CharField(max_length=20)
    placa = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    submarca = models.CharField(max_length=20)
    modelo = models.SmallIntegerField(blank=False)
    ultimo_holograma = models.CharField(max_length=20, blank=True, null=True, default='')
    coche_registrado = models.BooleanField(default=True)
    cupon = models.ForeignKey(Cupon, blank=True, null=True)
    operador = models.ForeignKey(Operador, related_name='solicitudes', blank=True, null=True, on_delete=models.SET_NULL)
    TYPE_CHOICES = (
        ('abierto', 'Abierto'),
        ('preagendado', 'Pre-Agendado'),
        ('agendado', 'Agendado'),
        ('proceso', 'En Proceso'),
        ('verificado', 'Verificado'),
        ('cerrado', 'Concluido'),
        ('caido', 'Cita Caída'),
        ('cancelado', 'Cancelado'),
        ('no_contratado', 'No Contratado'),
        ('reagendado', 'Reagendado'),
        ('pendiente', 'Pendiente'),
        ('abandonada', 'Abandonada'),
    )
    status = models.CharField(max_length=20, choices=TYPE_CHOICES, default='abierto')
    sent_reminder_email = models.BooleanField(default=False)
    linked_solicitudes = models.ForeignKey('self', blank=True, null=True, related_name='linkeadas', on_delete=models.SET_NULL)
    def __unicode__(self):
        return unicode(self.solicitudToken.deviceToken +' '+ self.status)
    def get_absolute_url(self):
        return reverse('drivemee:solicitud-detail', kwargs={'pk': self.folio})
    def internal_folio(self):
        return 10000321+self.pk
    def id(self):
        if self.status == 'abierto':
            return None
        return 10000321+self.pk
    
    class Meta:
        ordering = ['-timestamp_abierto']
        verbose_name_plural = 'Solicitudes'

class SnoozeReason(models.Model):
    solicitud = models.ForeignKey(Solicitud, related_name='snoozereasons', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    snoozed_until_date = models.DateTimeField(blank=False, null=False)
    motivo = models.CharField(max_length=200, blank=False, null=False)
    class Meta:
        verbose_name_plural = 'Razones'

class Note(models.Model):
    solicitud = models.ForeignKey(Solicitud, related_name='notas', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(max_length=500, blank=False, null=False)
    class Meta:
        verbose_name_plural = 'Notas'

class Documento(models.Model):
    solicitud = models.OneToOneField(Solicitud, related_name='documentos')
    adeudos = models.BooleanField(default=False)
    seguro = models.BooleanField(default=False)
    certificado = models.BooleanField(default=False)
    tarjeta = models.BooleanField(default=False)
    enterado = models.BooleanField(default=False)

class Direccion(models.Model):
    solicitud = models.ForeignKey(Solicitud, related_name='direcciones', null=True)
    calle = models.CharField(max_length=200, blank=False, null=False)
    numero_exterior = models.CharField(max_length=100, blank=True, null=True)
    numero_interior = models.CharField(max_length=100, blank=True, null=True)
    colonia = models.CharField(max_length=100, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    estado = MXStateField()
    codigo_postal = MXZipCodeField(blank=True, null=True)
    latitud = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    longitud = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    referencias = models.CharField(max_length=200, blank=True, null=True)
    CHOICES = (
        ('recoleccion', 'Recolección'),
        ('entrega', 'Entrega'),
        ('ambos', 'Ambos'),
    )
    tipo = models.CharField(max_length=11, choices=CHOICES)
    class Meta:
        verbose_name_plural = 'Direcciones'

class Cita(models.Model):
    solicitud = models.OneToOneField(Solicitud, related_name='cita')
    fecha = models.DateTimeField(blank=False)

class Evaluacion(models.Model):
    solicitud = models.OneToOneField(Solicitud, related_name='evaluacion')
    operador = models.ForeignKey(Operador, related_name='evaluaciones', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    comentarios = models.CharField(max_length=2500, null=True, blank=True)
    calificacion = models.DecimalField(blank=True, max_digits=3, decimal_places=2, null=True)
    no_quiso_calificar = models.BooleanField(default=False)
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Evaluaciones'

class Reporte(models.Model):
    solicitud = models.OneToOneField(Solicitud, related_name='reporte')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    motivo = models.CharField(max_length=250, null=False, blank=False)
    class Meta:
        ordering = ['-timestamp']

class Resultado(models.Model):
    solicitud = models.OneToOneField(Solicitud, related_name='resultado')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    VALORES = (
        ('DOBLE CERO', 'Doble Cero'),
        ('CERO', 'Cero'),
        ('UNO', 'Uno'),
        ('DOS', 'Dos'),
        ('RECHAZO', 'Rechazo'),
    )
    resultado = models.CharField(max_length=10, null=False, choices=VALORES, default='CERO')
    class Meta:
        ordering = ['-timestamp']

class CalificacionCliente(models.Model):
    client = models.ForeignKey(Client, related_name='calificaciones')
    solicitud = models.OneToOneField(Solicitud, related_name='calificacion')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    calificacion = models.DecimalField(blank=True, max_digits=3, decimal_places=2)
    motivo = models.CharField(max_length=250, null=False, blank=False)
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Calificaciones'

def create_solicitud_token(sender, instance, raw, **kwargs):
    if not instance.solicitudToken:
        token = SolicitudInternal.objects.create()
        token.save()
        instance.solicitudToken = token

signals.pre_save.connect(create_solicitud_token, sender=Solicitud, weak=False,
                          dispatch_uid='models.create_solicitud_token')
