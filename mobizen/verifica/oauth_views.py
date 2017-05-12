# -*- coding: utf-8 -*- 
from django.shortcuts import render
from django.views import generic
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route, list_route, api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import authentication

# from rest_framework.renderers import JSONRenderer
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from oauth2_provider.models import AccessToken

from verifica import serializers
from verifica import models
from verifica import push
from verifica import interesse
from verifica import imecas
from verifica import extra_permissions
from verifica import slackbot
from verifica import multa_parse
from verifica import placa_detector

from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta

import requests, json
import string
import random

def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def long_id_generator(size=32, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    # Para que siempre empiece con letras
    genId = ''.join(random.choice(string.ascii_lowercase) for _ in range(2))
    return genId + ''.join(random.choice(chars) for _ in range(size-2))

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Create your views here.

###
#
# Reglas HNC
class ContingenciaView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        today = timezone.now().date()
        tomorrow = today+relativedelta(days=+1)
        try:
            contingencia = models.Contingencia.objects.get(vigencia=today)
        except ObjectDoesNotExist:
            contingencia = None
        try:
            contingencia_tomorrow = models.Contingencia.objects.get(vigencia=tomorrow)
        except ObjectDoesNotExist:
            contingencia_tomorrow = None
        if not contingencia and not contingencia_tomorrow:
            return Response([])
        contingencias = []
        if contingencia:
            contingencias += [contingencia]
        if contingencia_tomorrow:
            contingencias += [contingencia_tomorrow]
        serializer = serializers.ContingenciaSerializer(contingencias, many=True)
        try:
            for c in serializer.data:
                c['reglas'][0].pop('semanas',None)
        except:
            pass
        return Response(serializer.data)

class ProgramaView(APIView):
    queryset = models.Programa.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            version = request.GET.get('version')
        except:
            return Response({'error':'missing version'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not version:
            return Response({'error':'missing version'},
                            status=status.HTTP_400_BAD_REQUEST)
        programa = models.Programa.objects.latest()
        if int(version) < programa.version:
            serializer = serializers.ProgramaSerializer(programa)
            return Response(serializer.data)
        return Response({'status':'ok'})

# Termina HNC
#
###
class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = serializers.SubscriptionSerializer(data=JSONParser().parse(request))
        if serializer.is_valid():
            return Response({'status':'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk=None):
        plazos = models.Plazo.objects.filter(enabled=True)
        paquetes = models.Paquete.objects.filter(enabled=True)
        plazo_serializer = serializers.PlazoSerializer(plazos, many=True)
        serializer = serializers.SubscriptionSerializer(self.request.user.client.account, many=false)
        return Response({'paquetes':paquete_serializer.data, 'plazos':plazo_serializer.data, 'control':[{'successURL':'https://autos.interesse.com.mx/autos/app/poliza/', 'errorURL':'https://autos.interesse.com.mx/autos/app/error/'}]})

class TarifaViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = models.Tarifa.objects.all()
    serializer_class = serializers.TarifaSerializer
    permission_classes = [IsAuthenticated]

class FeriadosView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        today = timezone.now().date()
        tomorrow = today + timedelta(1)
        feriados = {}
        try:
            feriado_today = models.Feriado.objects.filter(date=today)
        except:
            feriado_today = None
        try:
            feriado_tomorrow = models.Feriado.objects.filter(date=tomorrow)
        except:
            feriado_tomorrow = None
        if feriado_today:
            feriados.update({'today':True})
        else:
            feriados.update({'today':False})
        if feriado_tomorrow:
            feriados.update({'tomorrow':True})
        else:
            feriados.update({'tomorrow':False})
        return Response(feriados)

class ConfigView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        return Response({'kVerificaShouldShowUpsell':True,
                         'kVerificaShouldShowValet':True,
                         'kDriveMeeCallCenter':'5541426357'})

class PlacaView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            placa = request.GET.get('placa')
        except:
            return Response({'error':'missing parameter "placa"'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not placa:
            return Response({'error':'missing parameter "placa"'},
                            status=status.HTTP_400_BAD_REQUEST)
        check_type = request.GET.get('type')
        clean_placa = placa.replace(' ','').replace('-','')
        
        try:
            tipo_placa = placa_detector.parse_placa(clean_placa)
            serializer = serializers.PlacaSerializer(tipo_placa, many=False)
            return Response(serializer.data)
        except:
            return Response({'error':'Revisar Placa'},
                            status=status.HTTP_400_BAD_REQUEST)

class PlacaDetectorView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        try:
            placa = request.GET.get('placa')
        except:
            return Response({'error':'missing placa'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not placa:
            return Response({'error':'missing placa'},
                            status=status.HTTP_400_BAD_REQUEST)
        clean_placa = placa.replace(' ','').replace('-','')
        
        tipo = placa_detector.parse_placa(clean_placa)
        serializer = serializers.PlacaSerializer(tipo, many=False)
        return Response(serializer.data)

class VerificacionView(APIView):
    queryset = models.Vehiculo.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            placa = request.GET.get('placa')
        except:
            return Response({'error':'missing placa'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not placa:
            return Response({'error':'missing placa'},
                            status=status.HTTP_400_BAD_REQUEST)
        check_type = request.GET.get('type')
        clean_placa = placa.replace(' ','').replace('-','')
        
        if placa_detector.parse_placa(clean_placa).estado == 'DIF' or check_type == 'full':
            req = requests.get('http://datos.labplc.mx/movilidad/vehiculos/'+placa+'.json')
            try:
                data = req.json()
            except ValueError:
                return Response({'error':'parse error'},
                                status=status.HTTP_400_BAD_REQUEST)
            if 'consulta' in data:
                if check_type == 'full':
                    return Response(data)
                else:
                    consulta_dict = data.get('consulta')
                    if 'verificaciones' in consulta_dict and len(consulta_dict.get('verificaciones')) > 0:
                        verificaciones_list = consulta_dict.get('verificaciones')
                        if not verificaciones_list == u'intente_mas_tarde':
                            verificaciones_list[:] = [item for item in verificaciones_list if item.get('cancelado')=='NO']
                            if len(verificaciones_list) > 0:                    
                                sorted_list = sorted(verificaciones_list, key=lambda verificacion:verificacion.get('vigencia'), reverse=True)
                                vehiculo_info = sorted_list[0]
                                params = {'fecha_verificacion':vehiculo_info.get('fecha_verificacion'),
                                          'hora_verificacion':vehiculo_info.get('hora_verificacion'),
                                          'placa':vehiculo_info.get('placa'),
                                          'resultado':vehiculo_info.get('resultado'),
                                          'verificentro':vehiculo_info.get('verificentro'),
                                          'vigencia':vehiculo_info.get('vigencia'),
                                          'certificado':vehiculo_info.get('certificado'),
                                          'cancelado':'NO',
                                          }
                                return Response({'consulta':{'verificaciones':[params],}})
                            return Response({'error':'No hay verificaciones'},
                                            status=status.HTTP_400_BAD_REQUEST)
                        return Response({'error':'Timeout consulta'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    return Response({'error':'No hay verificaciones'},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response({'error':'remote error'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Estado incorrecto'},
                        status=status.HTTP_400_BAD_REQUEST)

class ImecasView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        data = cache.get('verifica.imecas_serialized')
        if not data:
            report = imecas.most_recent_report()
            serializer = serializers.ImecaSerializer(report, many=False)
            data = serializer.data
            cache.set('verifica.imecas_serialized', data, 30)
        return Response(data)

class MultaParserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        short_fundamento = multa_parse.parse_fundamento(request.GET.get('fundamento'))
        if not short_fundamento:
            short_fundamento = u'No se encuentra en el catálogo'
        return Response({'short_fundamento':short_fundamento})
    def post(self, request, format=None):
        serializer = serializers.MultaSerializer(data=JSONParser().parse(request))
        if serializer.is_valid():
            short_fundamento = multa_parse.parse_fundamento(serializer.data['fundamento'])
            return Response({'short_fundamento':short_fundamento})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class CotizadorViewSet(viewsets.ModelViewSet):
    queryset = models.Cotizacion.objects.all()
    serializer_class = serializers.CotizadorSerializer
    permission_classes = [IsAuthenticated]
    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def create(self, request, pk=None):
        serializer = serializers.CotizadorSerializer(data=request.data)
        if serializer.is_valid():
            if models.Aseguradora.objects.filter(name__icontains=serializer.data['aseguradora']):
                compania = models.Aseguradora.objects.filter(name__icontains=serializer.data['aseguradora'])[0]
            else:
                compania, created_aseguradora = models.Aseguradora.objects.get_or_create(name=serializer.data['aseguradora'])                
            paq = models.Paquete.objects.get(valor_interesse=serializer.data['paquete'])
            plz = models.Plazo.objects.get(valor_interesse=serializer.data['plazo'])
            cotizacion = models.Cotizacion(client=self.request.user.client,
                                           plazo=plz,
                                           paquete=paq,
                                           fecha=serializer.data['fecha'],
                                           costo=serializer.data['costo'],
                                           coche_registrado=serializer.data['coche_registrado'],
                                           aseguradora=compania)
            cotizacion.save()
            return Response({'cotizacionToken': cotizacion.deviceToken})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    # For POST Requests
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def log_error(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.CotizadorErrorSerializer(data=request.data)
        if serializer.is_valid():
            slackbot.send_message('Error al comprar cotizacion')
            error = models.CotizadorError(cotizacion=self.get_object(), descripcion=serializer.data['descripcion'])
            error.save()
            return Response({'status': 'error saved'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def log_recibo(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.ReciboSerializer(data=request.data)
        if serializer.is_valid():
            slackbot.send_message('Nuevo Recibo!')
            recibo = models.Recibo(cotizacion=self.get_object(), poliza=serializer.data['poliza'])
            recibo.save()
            return Response({'status': 'recibo saved'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class CotizadorView(APIView):
    model = models.Vehiculo
    queryset = models.Cotizacion.objects.all()
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = serializers.CotizacionSerializer(data=JSONParser().parse(request))
        if serializer.is_valid():
            serie = None
            if 'serie' in serializer.data:
                serie = serializer.data['serie']
            placa = None
            if 'placa' in serializer.data:
                placa = serializer.data['placa']
            deviceToken = None
            if 'deviceToken' in serializer.data:
                deviceToken = serializer.data['deviceToken']
            telefono = None
            if 'telefono' in serializer.data:
                telefono = serializer.data['telefono']
            nombre = None
            if 'nombre' in serializer.data:
                nombre = serializer.data['nombre']
            email = None
            if 'email' in serializer.data:
                email = serializer.data['email']
            descripcion = None
            if 'descripcion' in serializer.data:
                descripcion = serializer.data['descripcion']
            cotizacion = interesse.request_cotizacion(idAuto=serializer.data['idAuto'], cp=serializer.data['cp'], paquete=serializer.data['paquete'], plazo=serializer.data['plazo'], inicioVigencia=serializer.data['inicioVigencia'], codColonia=serializer.data['codColonia'], placa=placa, serie=serie, deviceToken=deviceToken, telefono=telefono, nombre=nombre, email=email, descripcion=descripcion)
            return Response(cotizacion)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk=None):
        plazos = models.Plazo.objects.filter(enabled=True)
        paquetes = models.Paquete.objects.filter(enabled=True)
        plazo_serializer = serializers.PlazoSerializer(plazos, many=True)
        paquete_serializer = serializers.PaqueteSerializer(paquetes, many=True)
        return Response({'paquetes':paquete_serializer.data, 'plazos':plazo_serializer.data, 'control':[{'successURL':'https://autos.interesse.com.mx/autos/app/poliza/', 'errorURL':'https://autos.interesse.com.mx/autos/app/error/'}]})

class AseguradoraViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = models.Aseguradora.objects.all()
    serializer_class = serializers.AseguradorasSerializer
    permission_classes = [IsAuthenticated]

class AppVersionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = models.AppVersion.objects.all()
    serializer_class = serializers.AppVersionSerializer
    permission_classes = [IsAuthenticated]

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = models.DeviceInfo.objects.all()
    serializer_class = serializers.DeviceUpdateSerializer
    permission_classes = [IsAuthenticated, extra_permissions.IsOwnerOnly]
    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def create(self, request, *args, **kwargs):
        try:
            device = models.DeviceInfo.objects.get(client=self.request.user.client, push_token=request.data.get('push_token'))
            return Response({'status':'Error: Ya existe este dispositivo', 'id':device.id}, status=status.HTTP_400_BAD_REQUEST)
        except:
            if 'deviceToken' in request.data:
                request.data.update({'deviceToken':self.request.user.client.pk})
            else:
                request.data['deviceToken']=self.request.user.client.pk
            return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
            
    def list(self, request):
        devices = self.request.user.client.device.all()
        serializer = serializers.DeviceUpdateSerializer(devices, many=True)
        return Response(serializer.data)
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def update_device(self, request, pk=None):
        device = self.get_object()
        serializer = serializers.DeviceUpdateSerializer(data=request.data)
        if serializer.is_valid():
            device.onesignal_token = serializer.data['onesignal_token']
            device.push_token = serializer.data['push_token']
            device.device_type = serializer.data['device_type']
            device.device_os = serializer.data['device_os']
            device.device_os_version = serializer.data['device_os_version']
            device.save()
            return Response({'status':'OK'})
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    @list_route(methods=['post'], permission_classes=[IsAuthenticated])
    def create_device(self, request, pk=None):
        serializer = serializers.DeviceUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                device = models.DeviceInfo.objects.get(client=self.request.user.client, push_token=serializer.data['push_token'])
                return Response({'status':'Error: Ya existe este dispositivo', 'id':device.id}, status=status.HTTP_400_BAD_REQUEST)
            except:
                device = models.DeviceInfo()
            device.client = self.request.user.client
            device.onesignal_token = serializer.data['onesignal_token']
            device.push_token = serializer.data['push_token']
            device.device_type = serializer.data['device_type']
            device.device_os = serializer.data['device_os']
            device.device_os_version = serializer.data['device_os_version']
            device.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        
class ClientViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsAuthenticated]
# auth
    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def list(self, request):
        serializer = serializers.ClientSerializer(self.request.user.client, many=False)
        return Response(serializer.data)
    # For GET Requests
    @list_route(methods=['get'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def status(self, request, pk=None):
        if validateEmail(self.request.user.email) == True:            
            return Response({'status':'OK'})
        return Response({'status':'Error: Invalid or No Email'}, status=status.HTTP_400_BAD_REQUEST)
    @list_route(methods=['get'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def devices(self, request, pk=None):
        devices = self.request.user.client.device.all()
        serializer = serializers.DeviceUpdateSerializer(devices, many=True)
        return Response(serializer.data)
    @list_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def update_email(self, request, pk=None):
        if not self.request.user.email == None and not self.request.user.email == '':
            return Response({'status':'Error: Client already has an email address'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.EmailSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            user.email = serializer.data['email']
            user.save()
            return Response({'status':'OK'})
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    @list_route(methods=['get'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def vehiculos(self, request, pk=None):
        vehiculos = self.request.user.client.vehiculos.all()
        serializer = serializers.VehiculoSerializer(vehiculos, many=True)
        return Response(serializer.data)
    @list_route(methods=['get'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def config(self, request, pk=None):
        config = [self.request.user.client.config]
        serializer = serializers.ConfigSerializer(config, many=True)
        return Response(serializer.data)
    @detail_route(methods=['get'], permission_classes=[IsAuthenticated])
    def notify(self, request, pk=None):
        push.send_push(self.get_object().deviceToken, push_time='now', alert='Actualiza!', badge=True, action='verifica.showNews', other=[{'title':'Actualiza', 'body':'Por favor descarga la version más nueva de Verifica', 'button':'Descargar', 'action':{'url':'https://beta.itunes.apple.com/v1/app/440844137?ct=MobizenSAdeCV&pt=2003'}}])
        return Response({'status': 'config updated'})
    def create(self, request, pk=None):
        if hasattr(self.request.user, 'client'):
            return Response({'status':'Error: Client already has a device token'},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'deviceToken' in request.data:
            try:
                a = models.Client.objects.get(deviceToken=request.data['deviceToken'])
                return Response({'status':'Error: Client already exists'},
                                status=status.HTTP_400_BAD_REQUEST)
            except:
                a = models.Client(deviceToken=request.data['deviceToken'])
        else:
            a = models.Client()
        a.appVersion = models.AppVersion.objects.all()[0]
        a.user = self.request.user
        a.save()
        return Response({'deviceToken': a.deviceToken})
    # For POST Requests
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def claim_token(self, request, pk=None):
        try:
            client = self.request.user.client
        except:
            client = None
        if not client == None:
            return Response({'Status':'Error: Client already has a device token'},
                            status=status.HTTP_400_BAD_REQUEST)
        client = self.get_object()
        if not client.user == None:
            return Response({'Error':'Unauthorized'},
                            status=status.HTTP_403_FORBIDDEN)
        client.user = self.request.user
        client.save()
        return Response({'Status': 'OK'})
    
    @list_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def update_config(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.ConfigSerializer(data=request.data)
        if serializer.is_valid():
            config = models.AppConfig.objects.update_or_create(client=self.request.user.client,
                                                               defaults={'alertas_hnc' : serializer.data['alertas_hnc'],
                                                                         'alertas_mnc' : serializer.data['alertas_mnc'],
                                                                         'hora_alertas_hnc' : serializer.data['hora_alertas_hnc'],
                                                                         'hora_alertas_mnc' : serializer.data['hora_alertas_mnc'],
                                                                         'hora_alertas_verificacion' : serializer.data['hora_alertas_verificacion']})
            return Response({'status': 'config updated'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @list_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def update_client(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.ClientUpdateSerializer(data=request.data)
        if serializer.is_valid():
            client = self.request.user.client
            client.last_login = timezone.now()
            client.save()
            oldVersion = client.appVersion
            maxVersion = models.AppVersion.objects.latest()
            try:
                currentVersion = models.AppVersion.objects.get(version=serializer.data['version'])
            except:
                currentVersion = None
            if currentVersion:
                try:
                    currentBuild = models.Builds.objects.get(number=serializer.data['build'])
                except:
                    currentBuild = None
                if currentBuild and currentBuild.version == currentVersion:
                    if currentBuild.isDebug and currentBuild.number < maxVersion.builds.latest().number:
                    # Si es debug y no es la mas reciente, pide actualizar
                        return Response({'status': 'debug', 'notas':[{'title':'Actualiza', 'body':'Por favor descarga la version más nueva de Verifica', 'button':'Descargar', 'actionTarget': 'https://beta.itunes.apple.com/v1/app/440844137?ct=MobizenSAdeCV&pt=2003', 'actionType':'url'}]})
                    if currentBuild.number == currentVersion.builds.latest().number and oldVersion == currentVersion:
                    # Contesta OK si es la mas reciente de la misma version
                        return Response({'status': 'OK'})
                    # Manda la build mas nueva para que el cliente guarde este valor y manda las build notes correspondientes
                    maxBuild = currentVersion.builds.latest()
                    response = serializers.BuildSerializer(maxBuild)
                    if not oldVersion == currentVersion:
                    # El cliente actualizo de version
                        client.appVersion = currentVersion
                        client.save()
                    return Response({'status':'news', 'notas': response.data['notas'], 'build':maxBuild.number})
            return Response({'status': 'debug'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @list_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def update_device(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.DeviceUpdateSerializer(data=request.data)
        if serializer.is_valid():
            client = self.request.user.client
            try:
                device = client.device
            except:
                device = models.DeviceInfo()
                device.client = client
            device.device_os = serializer.data.get('device_os')
            device.device_os_version = serializer.data.get('device_os_version')
            device.push_token = serializer.data.get('push_token')
            device.onesignal_token = serializer.data.get('onesignal_token')
            device.device_type = serializer.data.get('device_type')
            device.save()
            return Response({'status': 'OK'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class VehiculoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = models.Vehiculo.objects.all()
    serializer_class = serializers.VehiculoSerializer
    permission_classes = [IsAuthenticated, extra_permissions.IsOwnerOnly]
# auth
    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def list(self, request):
        try:
            vehiculos = self.request.user.client.vehiculos.all()
        except:
            vehiculos = None
        serializer = serializers.VehiculoSerializer(vehiculos, many=True)
        return Response(serializer.data)
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def create(self, request, *args, **kwargs):
        if 'deviceToken' in request.data:
            request.data.update({'deviceToken':self.request.user.client.pk})
        else:
            request.data['deviceToken']=self.request.user.client.pk
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
    def retrieve(self, request, pk=None):
        vehiculo = self.get_object()
        serializer = serializers.VehiculoSerializer(vehiculo)
        return Response(serializer.data)
    @detail_route(methods=['get'], permission_classes=[IsAuthenticated])
    def bla(self, request, pk=None):
        gr = self.get_object().fetch_info(send_push=True)
        return Response(gr)
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def verificar(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.VerificacionesSerializer(data=request.data)
        if serializer.is_valid():
            verificacion, created = models.Verificacion.objects.get_or_create(vehiculo=self.get_object())
            verificacion.vigencia = serializer.data['vigencia']
            if 'fecha' in serializer.data:
                verificacion.fecha = serializer.data['fecha']
            verificacion.resultado = serializer.data['resultado']
            verificacion.manual = True
            verificacion.save()
            return Response({'status': 'verificacion updated'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly], url_path='update')
    def update_vehiculo(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.VehiculoUpdateSerializer(data=request.data)
        if serializer.is_valid():
            vehiculo = self.get_object()
            vehiculo.alias = serializer.data['alias']
            if 'placa' in serializer.data and not vehiculo.placa == serializer.data['placa']:
                # cambio la placa, hay que borrar todo y volver a guardar
#                     push.send_push(deviceToken=vehiculo.client.deviceToken, alert='ahhhh!!')
                vehiculo.placa = serializer.data['placa']
                vehiculo.tenencias.all().delete()
                vehiculo.infracciones.all().delete()
                vehiculo.verificacion.all().delete()
                vehiculo.custom_modelo = False
                vehiculo.custom_car = False
                vehiculo.save()
                vehiculo.fetch_info()
            else:                
                if 'modelo' in serializer.data:
                    vehiculo.modelo = serializer.data['modelo']
                    vehiculo.custom_modelo = True
                if 'vin' in serializer.data:
                    vehiculo.vin = serializer.data['vin']
                if 'tarjeta_circulacion_permanente' in serializer.data:
                    vehiculo.tarjeta_circulacion_permanente = serializer.data['tarjeta_circulacion_permanente']
                if 'tarjeta_circulacion_vigencia' in serializer.data:
                    vehiculo.tarjeta_circulacion_vigencia = serializer.data['tarjeta_circulacion_vigencia']
                if 'codigo_postal' in serializer.data:
                    vehiculo.codigo_postal = serializer.data['codigo_postal']
                if 'query_string' in serializer.data:
                    vehiculo.query_string = serializer.data['query_string']
                if 'exento' in serializer.data:
                    vehiculo.exento = serializer.data['exento']
                vehiculo.save()
            return Response({'status': 'vehiculo updated'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def update_config(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.VehiculoConfigSerializer(data=request.data)
        if serializer.is_valid():
            config, created = models.VehiculoConfig.objects.update_or_create(vehiculo=self.get_object(),
                                                                            defaults={'alerta_inicio' : serializer.data['alerta_inicio'],
                                                                            'alerta_mes' : serializer.data['alerta_mes'],
                                                                            'alerta_quincena' : serializer.data['alerta_quincena'],
                                                                            'alerta_semana' : serializer.data['alerta_semana'],
                                                                            'alerta_fin' : serializer.data['alerta_fin']})
            return Response({'status': 'config updated'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def update_seguro(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.SeguroUpdateSerializer(data=request.data)
        if serializer.is_valid():
            aseguradora, created_aseguradora = models.Aseguradora.objects.get_or_create(name=serializer.data['aseguradora'])
            updated_values = {'aseguradora' : aseguradora, 'vigencia' : serializer.data['vigencia']}
            if 'titular' in serializer.data:
                updated_values['titular'] = serializer.data['titular']
            if 'poliza' in serializer.data:
                updated_values['poliza'] = serializer.data['poliza']
            if 'activo' in serializer.data:
                updated_values['activo'] = serializer.data['activo']            
            if 'boughtInApp' in serializer.data:
                updated_values['boughtInApp'] = serializer.data['boughtInApp']            
            if 'cobertura' in serializer.data:
                try:
                    paquete = models.Paquete.objects.get(valor_interesse=serializer.data['cobertura'])
                except:
                    paquete = None
                updated_values['cobertura'] = paquete
            seguro, created = models.Seguro.objects.update_or_create(vehiculo=self.get_object(), defaults=updated_values)
            return Response({'status': 'seguro updated'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def pago_tenencia(self, request, pk=None):
        """ Updates the object identified by the pk """
        if 'deviceToken' in request.data:
            request.data.update({'deviceToken':self.request.user.client.pk})
        else:
            request.data['deviceToken']=self.request.user.client.pk
        serializer = serializers.PagoTenenciaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                tenencia = models.Tenencia.objects.get(vehiculo=self.get_object(),periodo=request.data.get('tenencia'))
            except:
                return Response({'status': 'Tenencia not found'},status=status.HTTP_400_BAD_REQUEST)
            tenencia.delete()
            return Response({'status': 'tenencia updated'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def pago_infraccion(self, request, pk=None):
        """ Updates the object identified by the pk """
        if 'deviceToken' in request.data:
            request.data.update({'deviceToken':self.request.user.client.pk})
        else:
            request.data['deviceToken']=self.request.user.client.pk
        serializer = serializers.PagoInfraccionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                infraccion = models.Infraccion.objects.get(vehiculo=self.get_object(),folio=str(request.data.get('folio_infraccion')))
            except:
                return Response({'status': 'Infraccion not found'},status=status.HTTP_400_BAD_REQUEST)
            infraccion.situacion = 'Pagada'
            infraccion.forced_pago = True
            infraccion.save()
            return Response({'status': 'infraccion updated'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def delete(self, request, pk=None):
        """ Updates the object identified by the pk """
        vehiculo=self.get_object()
        vehiculo.placa = vehiculo.placa+'_'+vehiculo.client.deviceToken+id_generator()
        client, created = models.Client.objects.get_or_create(deviceToken='admin')
        vehiculo.client = client
        vehiculo.save()
        return Response({'status': 'vehiculo deleted'})

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated, extra_permissions.IsOwnerOnly])
    def upload_image(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
#            serializer.save()
           vehiculo = self.get_object()
           vehiculo.image = request.FILES['image']
           vehiculo.save()
           return Response({'status':'Upload OK'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)