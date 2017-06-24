# -*- coding: utf-8 -*- 
import datetime
import string
import unicodedata
from django.utils import timezone
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.conf import settings

import requests, json
from random_primary import RandomPrimaryIdModel
from verifica.client_manager import ClientManager
from verifica.cotizador_manager import CotizadorManager
from verifica.vehiculo_manager import VehiculoManager
from localflavor.mx.models import MXStateField
from verifica import multa_parse
from services import ApiGobInfoConsumer

# Create your models here.
###
# Reglas Hoy No Circula


class Terminacion(models.Model):
    value = models.CharField(max_length=1, blank=False, unique=True)
    def __unicode__(self):
        return self.value
    class Meta:
        ordering = ['value']

class Holograma(models.Model):
    VALORES = (
        ('DOBLE CERO', 'Doble Cero'),
        ('CERO', 'Cero'),
        ('UNO', 'Uno'),
        ('DOS', 'Dos'),
        ('EXENTO', 'Exento'),
    )
    value = models.CharField(max_length=10, null=False, choices=VALORES, unique=True)
    def __unicode__(self):
        return self.value
    class Meta:
        ordering = ['value']

class Semana(models.Model):
    value = models.SmallIntegerField(blank=False, unique=True)
    title = models.CharField(max_length=20, blank=False)
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ['value']

class ReglaCirculacion(models.Model):
    terminaciones = models.ManyToManyField(Terminacion)    
    hologramas = models.ManyToManyField(Holograma)
    semanas = models.ManyToManyField(Semana, null=True, blank=True)
    title = models.CharField(max_length=50, blank=False)
    def __unicode__(self):
        return self.title

class Dia(models.Model):
    value = models.SmallIntegerField(blank=False)
    title = models.CharField(max_length=50, blank=False)
    day_name = models.CharField(max_length=20, blank=False, default='')
    reglas = models.ManyToManyField(ReglaCirculacion)
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ['value']

class Contingencia(models.Model):
    title = models.CharField(max_length=50, blank=False)
    vigencia = models.DateField(blank=False)
    reglas = models.ManyToManyField(ReglaCirculacion, blank=False)
    def __unicode__(self):
        return self.title

class Programa(models.Model):
    version = models.SmallIntegerField(blank=False)
    dias = models.ManyToManyField(Dia)
    vigencia_inicio = models.DateField(blank=False)
    vigencia_fin = models.DateField(blank=False)
    title = models.CharField(max_length=50, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ['version']
        get_latest_by = "timestamp"
# Terminan Reglas Hoy No Circula
###

class TipoPlaca(models.Model):
    CHOICES = (
        ('Particular', 'Particular'),
        ('Discapacitado', 'Discapacitado'),
        ('Motocicleta', 'Motocicleta'),
        ('Taxi', 'Taxi'),
    )
    tipo = models.CharField(max_length=20, choices=CHOICES)
    estado = MXStateField(null=True)
    def __unicode__(self):
        return self.tipo
    class Meta:
        unique_together = (("estado", "tipo"),)

# class Regla(models.Model):
#     hoy_no_circula = models.BooleanField(default=False)
#     hoy_no_circula_sabatino = models.BooleanField(default=False)
#     verificacion = models.BooleanField(default=False)
#     placa = models.OneToOneField(TipoPlaca)
# 
# class ReglaEntidad(models.Model):
#     hoy_no_circula_sabatino = models.BooleanField(default=False)
    



class Feriado(models.Model):
    date = models.DateField(blank=False)
    def __unicode__(self):
        return str(self.date)

class Aseguradora(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __unicode__(self):
        return self.name

class Imeca(models.Model):
    imecas = models.CharField(max_length=4, blank=False)
    particula = models.CharField(max_length=15)
    indice_uv = models.CharField(max_length=4, blank=True, null=True)
    hora = models.CharField(max_length=2, default='0', blank=False)
    fecha = models.DateField(blank=False)
    class Meta:
        unique_together = (("fecha", "hora"),)
    def __unicode__(self):
        return str(self.fecha) + ' ' + self.hora
    class Meta:
        ordering = ['-pk', '-fecha']

class Paquete(models.Model):
    nombre = models.CharField(max_length=100, blank=False, unique=True)
    valor_interesse = models.SmallIntegerField(unique=True)
    enabled = models.BooleanField(default=True, blank=False)
    internal_order = models.SmallIntegerField(unique=True, blank=True, null=True)
    def __unicode__(self):
        return self.nombre
    class Meta:
        ordering = ['internal_order']

class Plazo(models.Model):
    nombre = models.CharField(max_length=100, blank=False, unique=True)
    valor_interesse = models.SmallIntegerField(unique=True)
    enabled = models.BooleanField(default=True, blank=False)
    def __unicode__(self):
        return self.nombre
    class Meta:
        ordering = ['valor_interesse']

class AppVersion(models.Model):
    version = models.CharField(max_length=10, blank=True)
    title = models.CharField(max_length=30, blank=True)
    def __unicode__(self):
        return self.title+' ('+self.version +')'
    class Meta:
        get_latest_by = 'version'
        ordering = ['-version']

class Builds(models.Model):
    version = models.ForeignKey(AppVersion, related_name='builds')    
    number = models.IntegerField(unique=True)
    isDebug = models.BooleanField(default=False)
    class Meta:
        get_latest_by = 'number'
        ordering = ['number']

class BuildNote(models.Model):
    title = models.CharField(max_length=255,blank=True)
    body = models.CharField(max_length=255,blank=True)
    build = models.ForeignKey(Builds, related_name='notas')
    button = models.CharField(max_length=50,blank=False)
    actionTarget = models.CharField(max_length=255,blank=True)
    TYPE_CHOICES = (
        ('dismiss', 'Dismiss View'),
        ('url', 'Open Link'),
        ('none', 'No Action'),
    )
    actionType = models.CharField(max_length=20, choices=TYPE_CHOICES, default='dismiss')

class ReleaseNotes(models.Model):
    title = models.CharField(max_length=255,blank=True)
    body = models.CharField(max_length=255,blank=True)
    version = models.ForeignKey(AppVersion, related_name='notas')
    button = models.CharField(max_length=50,blank=False)
    actionTarget = models.CharField(max_length=255,blank=True)
    TYPE_CHOICES = (
        ('dismiss', 'Dismiss View'),
        ('url', 'Open Link'),
        ('none', 'No Action'),
    )
    actionType = models.CharField(max_length=20, choices=TYPE_CHOICES, default='dismiss')

class Subscription(models.Model):
    expired = models.BooleanField(default=False)
    expiration_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(auto_now_add=True, blank=True)
    SOURCE_CHOICES = (
        ('appstore', 'Apple App Store'),
        ('playstore', 'Google Play Store'),
        ('other', 'Other'),
    )
    sub_source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='other')
    gps_token = models.CharField(max_length=200,blank=True,default=None,null=True)
    gps_subscriptionId = models.TextField(blank=True,default=None,null=True)
    gps_packageName = models.TextField(blank=True,default=None,null=True)
    ios_receipt = models.TextField(blank=True, null=True)
    ios_password = models.TextField(blank=True,default=None,null=True)
    autoRenewing = models.BooleanField(default=False)
    expiryTimeMillis = models.BigIntegerField(blank=True, null=True)
    startTimeMillis = models.BigIntegerField(blank=True, null=True)

class AccountType(models.Model):
    FREE = 'free'
    PAID = 'paid'
    ACC_TYPE_CHOICES = (
        (FREE, 'Free User'),
        (PAID, 'Paid User'),
    )
    expiration_time = models.DateTimeField(blank=True, null=True)
    account_type = models.CharField(max_length=20, choices=ACC_TYPE_CHOICES, default=FREE)
    subscriptions = models.ForeignKey(Subscription, null=True, related_name='owner')
    def is_sub_active(self):
        return False
    
class Client(RandomPrimaryIdModel):
    #id = models.CharField(max_length=30, unique=False, null=True)
    #deviceToken = models.CharField(max_length=100, unique=True, primary_key=True)
    appVersion = models.ForeignKey(AppVersion, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    last_login = models.DateTimeField(blank=True, default=None, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='client')
    account = models.OneToOneField(AccountType, null=True, blank=True, related_name='client')
    objects = ClientManager()
    def __unicode__(self):
        return self.deviceToken
    class Meta:
        ordering = ['-timestamp']

class DeviceInfo(models.Model):
    onesignal_token = models.CharField(max_length=100,blank=True,default=None,null=True)
    parse_token = models.CharField(max_length=100,blank=True,default=None,null=True)
    push_token = models.CharField(max_length=200,blank=True,default=None,null=True)
    device_type = models.CharField(max_length=100,blank=True,default=None,null=True)
    device_os = models.CharField(max_length=10,blank=True,default=None,null=True)
    device_os_version = models.CharField(max_length=10,blank=True,default=None,null=True)
    client = models.ForeignKey(Client, null=False, related_name='device')

class DriverInfo(models.Model):
    is_primary = models.BooleanField(default=False)
    name = models.CharField(max_length=250,blank=True,default=None,null=True)
    vigencia_licencia = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='verifica/clients/drivers/', blank=True, null=True)
    client = models.ForeignKey(Client, null=False, related_name='drivers')

class Manufacturer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __unicode__(self):
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=50, unique=False)
    manufacturer = models.ForeignKey(Manufacturer)
    def __unicode__(self):
        return self.name
    @classmethod
    def update_create(cls, marca, submarca):
        manufacturer = Manufacturer.objects.get_or_create(name=marca)
        car = Car.objects.get_or_create(name=submarca, manufacturer=manufacturer)
        return car
    class Meta:
        unique_together = (("name", "manufacturer"),)

class Vehiculo(models.Model):
    client = models.ForeignKey(Client, related_name='vehiculos')
    car = models.ForeignKey(Car, blank=True, null=True)
    alias = models.CharField(max_length=50, null=True)
    placa = models.CharField(max_length=30, blank=True)
    modelo = models.SmallIntegerField(blank=True, null=True)
    vin = models.CharField(max_length=20, blank=True)
    tarjeta_circulacion_permanente = models.BooleanField(default=False)
    tarjeta_circulacion_vigencia = models.DateField(blank=True, null=True)
    codigo_postal = models.CharField(max_length=5, blank=True)
    query_string = models.CharField(max_length=100, blank=True)
    exento = models.BooleanField(default=False)
    es_par = models.BooleanField(default=False)
    dia_no_circula = models.SmallIntegerField(default=5)
    custom_modelo = models.BooleanField(default=False)
    custom_car = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    objects = VehiculoManager()
    did_fetch_info = models.BooleanField(default=False)
    ultimo_digito = models.CharField(max_length=1, blank=True)
    image = models.ImageField(upload_to='verifica/clients/vehiculos/', blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (("client", "placa"),)
    def __unicode__(self):
        return unicode(self.alias)
    def fetch_info(self, send_push=False, save_tenencias=False, tipo=''):
        placa = self.placa.replace(' ','').replace('-','')
        try:
            data = ApiGobInfoConsumer(placa).get(tipo)
        except ValueError:
#             raise requests.exceptions.RequestException(req)
            return False
        if 'consulta' in data:
            consulta_dict = data.get('consulta')
            if save_tenencias == True or self.did_fetch_info == False:
                if 'tenencias' in consulta_dict:
                    self.did_fetch_info = True
                    tenencias_list = consulta_dict.get('tenencias')
                    try:                    
                        adeudos = tenencias_list.get('adeudos').split(',')
                    except:
                        adeudos = []
                    for year in adeudos:
                        t, created = Tenencia.objects.get_or_create(vehiculo=self, periodo=year)
                        t.save()
            if 'infracciones' in consulta_dict and len(consulta_dict.get('infracciones')) > 0:
                infracciones_list = consulta_dict.get('infracciones')
                for inf in infracciones_list:
                    try:
                        folio = inf.get('folio')
                    except:
                        continue
                    if Infraccion.objects.filter(vehiculo=self, folio=folio).exists():
                        i = Infraccion.objects.get(vehiculo=self, folio=folio)
#                         if not i.short_fundamento:
                        i.short_fundamento = multa_parse.parse_fundamento(i.fundamento)
                        if len(i.sancion.split()) > 1:
                            i.sancion = multa_parse.parse_sancion(i.sancion)
                        if inf.get('situacion') == 'EXIMIDA':
                            i.situacion = 'Pagada'
                        if i.forced_pago == False and not i.situacion == inf.get('situacion') and not inf.get('situacion') == 'EXIMIDA':
                            i.situacion = inf.get('situacion')
                        i.save()
#                             if send_push == True:
#                                 push.send_push(deviceToken=self.client.deviceToken, alert=u'Se detectó el pago de una infracción para el auto '+self.alias+u'.', action='verifica.showInfo', vehiculo=self.id, sound=' ')
                    else:
                        i = Infraccion(vehiculo=self,
                                       folio=folio,
                                       fecha=inf.get('fecha'),
                                       situacion=inf.get('situacion'),
                                       motivo=inf.get('motivo'),
                                       fundamento=inf.get('fundamento'),
                                       sancion=inf.get('sancion'))
                        if not i.motivo:
                            i.motivo = u'Descripción No Disponible'
                        i.short_fundamento = multa_parse.parse_fundamento(i.fundamento)
                        i.sancion = multa_parse.parse_sancion(inf.get('sancion'))
                        i.save()
#                         if send_push==True:
#                             push.send_push(deviceToken=self.client.deviceToken, alert=u'Se detectó una nueva infracción para el auto '+self.alias+u'.', action='verifica.showInfo', vehiculo=self.id, sound=' ')
            if 'verificaciones' in consulta_dict and len(consulta_dict.get('verificaciones')) > 0:
                verificaciones_list = consulta_dict.get('verificaciones')
                if not verificaciones_list == u'intente_mas_tarde' and not verificaciones_list == u'error':
                    verificaciones_list[:] = [item for item in verificaciones_list if not item.get('resultado')=='RECHAZO']
                    if len(verificaciones_list) > 0:                    
                        sorted_list = sorted(verificaciones_list, key=lambda verificacion:verificacion.get('vigencia'), reverse=True)
                        vehiculo_info = sorted_list[0]
                        self.vin = vehiculo_info.get('vin')
                        if self.custom_modelo == False:
                            self.modelo = vehiculo_info.get('modelo')
                        if self.custom_car == False:
                            manufacturer, created=Manufacturer.objects.get_or_create(name=vehiculo_info.get('marca'))
                            car, created_car = Car.objects.get_or_create(name=vehiculo_info.get('submarca'), manufacturer=manufacturer)
                            self.car = car
                        verificacion, created_verificacion = Verificacion.objects.get_or_create(vehiculo=self)
                        if not created_verificacion:
                            if datetime.datetime.strptime(vehiculo_info.get('vigencia'), '%Y-%m-%d').date() > verificacion.vigencia:
                                # Se detecto una nueva verificacion
                                verificacion.vigencia = vehiculo_info.get('vigencia')
                                verificacion.resultado = vehiculo_info.get('resultado')
                                verificacion.fecha = vehiculo_info.get('fecha_verificacion')
                                verificacion.manual = False
                                if send_push == True:
                                    push.send_push(deviceToken=self.client.deviceToken, alert=u'Verificación del auto '+self.alias+u' detectada. Consulta próximo periodo', action='verifica.showInfo', vehiculo=self.id, sound=' ')
                            elif verificacion.manual == False:
                                verificacion.vigencia = vehiculo_info.get('vigencia')
                                verificacion.resultado = vehiculo_info.get('resultado')
                                verificacion.fecha = vehiculo_info.get('fecha_verificacion')
                        else:
                            verificacion.vigencia = vehiculo_info.get('vigencia')
                            verificacion.resultado = vehiculo_info.get('resultado')
                            verificacion.fecha = vehiculo_info.get('fecha_verificacion')
                        verificacion.save()
            self.last_update = timezone.now()
            self.save()
        self.fix_yo_shit()
        return True
#         return req.json()
    def fix_yo_shit(self):
        self.set_par()
        self.que_dia_no_circula()
        self.set_ultimo_digito()
    def set_ultimo_digito(self):
        placa = unicodedata.normalize('NFKD', self.placa).encode('ascii','ignore')
        placa = placa.replace(' ','').replace('-','')
        digitos = placa.translate(None, string.letters)
        if len(digitos) == 0:
            self.ultimo_digito = u'0'
        elif len(digitos)>1:
            self.ultimo_digito = digitos[-1:]
        else:
            self.ultimo_digito = digitos[0]
        self.save()
    def set_par(self):
        placa = unicodedata.normalize('NFKD', self.placa).encode('ascii','ignore')
        placa = placa.replace(' ','').replace('-','')
        digitos = placa.translate(None, string.letters)
        if len(digitos) == 0:
            return
        if len(digitos)>1:
            ultimo = int(digitos[-1:])
        else:
            ultimo = int(digitos[0])
        if ultimo % 2 > 0:
            self.es_par = False
        else:
            self.es_par = True
        self.save()
    def que_dia_no_circula(self):
        placa = unicodedata.normalize('NFKD', self.placa).encode('ascii','ignore')
        placa = placa.replace(' ','').replace('-','')
        digitos = placa.translate(None, string.letters)
        if len(digitos) == 0:
            return
        if len(digitos)>1:
            ultimo = int(digitos[-1:])
        else:
            ultimo = int(digitos[0])
        dia = 4
        if ultimo == 0 or ultimo == 9:
            dia = 4
        elif ultimo == 1 or ultimo == 2:
            dia = 3
        elif ultimo == 3 or ultimo == 4:
            dia = 2
        elif ultimo == 5 or ultimo == 6:
            dia = 0
        elif ultimo == 7 or ultimo == 8:
            dia = 1
        self.dia_no_circula = dia
        self.save()

class VehiculoConfig(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, unique=True, null=False, related_name='config')
    alerta_inicio = models.BooleanField(default=True)
    alerta_mes = models.BooleanField(default=True)
    alerta_quincena = models.BooleanField(default=True)
    alerta_semana = models.BooleanField(default=True)
    alerta_fin = models.BooleanField(default=True)
    
class Tenencia(models.Model):
    periodo = models.SmallIntegerField(default=0)
    vehiculo = models.ForeignKey(Vehiculo, related_name='tenencias')
    class Meta:
        unique_together = (("vehiculo", "periodo"),)

class Infraccion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, related_name='infracciones')
    folio = models.CharField(max_length=50)
    fecha = models.DateField()
    SITUACION_CHOICES = (
        ('Pagada', 'Pagada'),
        ('No Pagada', 'No Pagada'),
    )
    situacion = models.CharField(max_length=30, choices=SITUACION_CHOICES, default='NO')
    motivo = models.CharField(max_length=300)
    fundamento = models.CharField(max_length=255)
    short_fundamento = models.CharField(max_length=50, blank=True, null=True)
    sancion = models.CharField(max_length=50)
    forced_pago = models.BooleanField(default=False)
    @classmethod
    def create(cls, folio, fecha, situacion, motivo, fundamento, sancion, vehiculo):
        infraccion = cls(folio=folio, fecha=fecha, situacion=situacion, motivo=motivo, fundamento=fundamento, sancion=sancion, vehiculo=vehiculo)
        return infraccion
    class Meta:
        unique_together = (("vehiculo", "folio"),)
        ordering = ['-fecha']

class Verificacion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, related_name='verificacion', unique=True)
    resultado = models.CharField(max_length=10, blank=True)
    fecha = models.DateField(blank=True, null=True)
    vigencia = models.DateField(blank=True, null=True)
    manual = models.BooleanField(default=False)    

class Seguro(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, unique=True, null=True, related_name='seguro')
    poliza = models.CharField(max_length=30, null=True, blank=True)
    titular = models.CharField(max_length=100, blank=True, null=True)
    vigencia = models.DateField(null=True)
    aseguradora = models.ForeignKey(Aseguradora, null=True, blank=True)
    activo = models.BooleanField(default=True)
    boughtInApp = models.BooleanField(default=False)
    cobertura = models.ForeignKey(Paquete, null=True, blank=True)

class AppConfig(models.Model):
    alertas_hnc = models.BooleanField(default=True)
    alertas_mnc = models.BooleanField(default=True)
    hora_alertas_verificacion = models.CommaSeparatedIntegerField(max_length=5, default='10,30', null=False)
    hora_alertas_hnc = models.CommaSeparatedIntegerField(max_length=5, default='5,00', null=False)
    hora_alertas_mnc = models.CommaSeparatedIntegerField(max_length=5, default='22,00', null=False)
    client = models.OneToOneField(Client, null=False, related_name='config')

class Telefono(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    telnumber = models.CharField(max_length=30, null=True, blank=True)
    aseguradora = models.ForeignKey(Aseguradora, related_name='telefonos')
    class Meta:
        unique_together = (("aseguradora", "telnumber"),)

class Costo(models.Model):
    aseguradora = models.ForeignKey(Aseguradora, null=True, blank=True)
    costo = models.CharField(max_length=10, blank=False, default='0')
    def __unicode__(self):
        return self.aseguradora.name + ', $' + self.costo

class Comparacion(models.Model):
    # deviceToken va a ser el id de la cotizacion
    client = models.ForeignKey(Client, related_name='comparaciones', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    plazo = models.ForeignKey(Plazo)
    paquete = models.ForeignKey(Paquete)
    fecha = models.DateField(blank=False)
    coche_registrado = models.BooleanField(default=True, blank=False)
    id_auto = models.CharField(max_length=10, null=True, blank=True)
    codigo_colonia = models.CharField(max_length=10, null=True, blank=True)
    codigo_postal = models.CharField(max_length=6, null=True, blank=True)
    costos = models.ManyToManyField(Costo, null=True)
    elapsed = models.DecimalField(max_digits=5, decimal_places=3, default=0.0)
    timeout = models.BooleanField(default=False, blank=False)
    error_message = models.CharField(max_length=250, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    descripcion = models.CharField(max_length=250, null=True, blank=True)
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Comparaciones'

class Cotizacion(RandomPrimaryIdModel):
    # deviceToken va a ser el id de la cotizacion
    client = models.ForeignKey(Client, related_name='cotizaciones')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    plazo = models.ForeignKey(Plazo, related_name='recibos')
    paquete = models.ForeignKey(Paquete, related_name='recibos')
    fecha = models.DateField(blank=False)
    costo = models.CharField(max_length=10, blank=False, default='0')
    coche_registrado = models.BooleanField(default=True, blank=False)
    aseguradora = models.ForeignKey(Aseguradora, null=True, blank=True)
    objects = CotizadorManager()
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Cotizaciones'

class CotizadorError(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, related_name='errores')
    descripcion = models.CharField(max_length=255, default=True, blank=False)

class Recibo(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, related_name='recibos')
    poliza = models.CharField(max_length=100, blank=False)
    cancelado = models.BooleanField(default=False, blank=False)
    seguro = models.ForeignKey(Seguro, null=True, blank=True, related_name='recibo')
    vehiculo = models.ForeignKey(Vehiculo, null=True, blank=True, related_name='recibo')

class SalarioMinimo(models.Model):
    tipo = models.CharField(max_length=4, blank=False, unique=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def __unicode__(self):
        return self.tipo

class Tarifa(models.Model):
    estado = MXStateField()
    salario_minimo = models.ForeignKey(SalarioMinimo)
    footer = models.CharField(max_length=250, blank=True, null=True)
    def __unicode__(self):
        return self.estado
    class Meta:
        ordering = ['estado']

class TarifaItem(models.Model):
    order = models.SmallIntegerField()
    tarifa = models.ForeignKey(Tarifa, related_name='items')
    name = models.CharField(max_length=255, default=True, blank=False)
    costo = models.CharField(max_length=12, default=True, blank=False)
    class Meta:
        ordering = ['order']
        unique_together = (("tarifa", "order"),)

def create_client_config(sender, instance, created, **kwargs):
    """Create AppConfig for every new Client."""
    if created:
        AppConfig.objects.create(client=instance)

signals.post_save.connect(create_client_config, sender=Client, weak=False,
                          dispatch_uid='models.create_client_config')

def create_vehiculo_config(sender, instance, created, **kwargs):
    """Create VehiculoConfig for every new Vehiculo."""
    if created:
        VehiculoConfig.objects.create(vehiculo=instance)

signals.post_save.connect(create_vehiculo_config, sender=Vehiculo, weak=False,
                          dispatch_uid='models.create_vehiculo_config')

def fetch_cdmx_info(sender, instance, created, **kwargs):
    """Create VehiculoConfig for every new Vehiculo."""
    if created:
        instance.fix_yo_shit()
#         instance.fetch_info(save_tenencias=True)


signals.post_save.connect(fetch_cdmx_info, sender=Vehiculo, weak=False,
                          dispatch_uid='models.fetch_cdmx_info')

from verifica import push
