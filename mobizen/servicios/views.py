# -*- coding: utf-8 -*- 
from django.shortcuts import render
from django.views import generic
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

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

from servicios import serializers
from servicios import models
from verifica import extra_permissions


# class CotizadorView(APIView):
#     model = models.Servicio
#     queryset = models.Servicio.objects.all()
#     permission_classes = (extra_permissions.AuthOnlyModelPermissions,)
#     def update(self, request, pk=None):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def partial_update(self, request, pk=None):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def destroy(self, request, pk=None):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def post(self, request, format=None):
#         serializer = serializers.CotizacionSerializer(data=JSONParser().parse(request))
#         if serializer.is_valid():
#             serie = None
#             if 'serie' in serializer.data:
#                 serie = serializer.data['serie']
#             placa = None
#             if 'placa' in serializer.data:
#                 placa = serializer.data['placa']
#             cotizacion = interesse.request_cotizacion(idAuto=serializer.data['idAuto'], cp=serializer.data['cp'], paquete=serializer.data['paquete'], plazo=serializer.data['plazo'], inicioVigencia=serializer.data['inicioVigencia'], codColonia=serializer.data['codColonia'], placa=placa, serie=serie)
#             return Response(cotizacion)
#         else:
#             return Response(serializer.errors,
#                             status=status.HTTP_400_BAD_REQUEST)
#     def get(self, request, pk=None):
#         plazos = models.Plazo.objects.filter(enabled=True)
#         paquetes = models.Paquete.objects.filter(enabled=True)
#         plazo_serializer = serializers.PlazoSerializer(plazos, many=True)
#         paquete_serializer = serializers.PaqueteSerializer(paquetes, many=True)
#         return Response({'paquetes':paquete_serializer.data, 'plazos':plazo_serializer.data, 'control':[{'successURL':'https://autos.interesse.com.mx/autos/app/poliza/', 'errorURL':'https://autos.interesse.com.mx/autos/app/error/'}]})

class ServicioViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = models.Servicio.objects.all()
    serializer_class = serializers.ServicioSerializer
    permission_classes = (extra_permissions.AuthOnlyModelPermissions,)
    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def list(self, request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        queryset = models.Establecimiento.objects.filter(servicio__name=pk)
        serializer = serializers.EstablecimientoSerializer(queryset, many=True)
        return Response(serializer.data)
        
    
#         vehiculo = self.get_object()
#         serializer = serializers.VehiculoSerializer(vehiculo)
#         if 'deviceToken' in request.query_params:
#             token = request.query_params['deviceToken']
#             if vehiculo.client.deviceToken == token:
#                 return Response(serializer.data)
#             else:
#                 return Response({'status':'Incorrect Device Token'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'status':'Missing Device Token'},
#                             status=status.HTTP_400_BAD_REQUEST)

