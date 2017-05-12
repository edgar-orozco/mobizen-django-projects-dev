from django.db import models
from django.utils import timezone
from django.db.models import signals
from localflavor.mx.models import MXStateField, MXZipCodeField

import datetime
import string
import unicodedata

# Create your models here.

class Estado(models.Model):
    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=12, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Municipio(models.Model):
    name = models.CharField(max_length=50)
    estado = MXStateField()
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Colonia(models.Model):
    name = models.CharField(max_length=50)
    municipio = models.ForeignKey(Municipio, related_name='colonias')
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['municipio__name', 'name']

class CodigoPostal(models.Model):
    name = models.CharField(max_length=5, unique=True)
    def __unicode__(self):
        return self.name

class Tramite(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __unicode__(self):
        return self.name

class Servicio(models.Model):
    name = models.CharField(max_length=50, unique=True)
    enabled = models.BooleanField(default=True)
    version = models.IntegerField(default=0, blank=False)
    def __unicode__(self):
        return self.name

class Telefono(models.Model):
    telnumber = models.CharField(max_length=30, unique=True, blank=False)
    def __unicode__(self):
        return self.telnumber

class Establecimiento(models.Model):
    identificador = models.CharField(max_length=50)
    razon_social = models.CharField(max_length=100, blank=True)
    tramites = models.ManyToManyField(Tramite, blank=True)
    servicio = models.ForeignKey(Servicio, related_name='establecimientos')
    enabled = models.BooleanField(default=True)
    telefonos = models.ManyToManyField(Telefono, null=True, blank=True)
    acepta_descuento = models.BooleanField(default=False)
    def __unicode__(self):
        return self.razon_social + ' - ' + self.identificador

class Direccion(models.Model):
    calle = models.CharField(max_length=200)
    estado = MXStateField()
    municipio = models.ForeignKey(Municipio)
    colonia = models.ForeignKey(Colonia)
    codigo_postal = MXZipCodeField(blank=True)
    latitud = models.DecimalField(max_digits=20, decimal_places=7, blank=False)
    longitud = models.DecimalField(max_digits=20, decimal_places=7, blank=False)
    establecimiento = models.OneToOneField(Establecimiento, blank=True, null=True)
    
