# -*- coding: utf-8 -*- 

# from django.shortcuts import render
# from django.views import generic
# from django.views.generic import FormView
# from django.views.generic.base import TemplateView
# from django.contrib import messages
# from django.utils import timezone
# from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated

# from rest_framework import generics
# from rest_framework import permissions
# from rest_framework import filters
# from rest_framework import renderers
# from rest_framework import viewsets
from rest_framework import status
# from rest_framework.decorators import detail_route, list_route, api_view, authentication_classes
from rest_framework.response import Response
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
# from rest_framework import authentication
# from rest_framework.renderers import JSONRenderer

from verifica import serializers
from verifica import models
from verifica import push
from verifica import extra_permissions

def parse_recibo(recibo=None, poliza_status='', seguro=None):
    if recibo:
        if poliza_status == 'cancelado':
            recibo.cancelado = True
            if seguro:
            # Guarda el vehiculo y seguro en el recibo para poder reestablecerlos en caso de que se vuelva a activar
                recibo.vehiculo = seguro.vehiculo
                recibo.seguro = seguro
                seguro.vehiculo = None
                seguro.save()
            recibo.save()
            return Response({'status':'OK: Poliza cancelada'}, status=status.HTTP_200_OK)
        elif poliza_status == 'activo':
            recibo.cancelado = False
            if recibo.seguro:
            # Reestablece el seguro al vehiculo original
                seguro = recibo.seguro
                seguro.vehiculo = recibo.vehiculo
                seguro.activo = True
                seguro.aseguradora = recibo.cotizacion.aseguradora
                seguro.save()
                recibo.vehiculo = None
                recibo.seguro = None
#                 push.send_push(deviceToken=seguro.vehiculo.client.deviceToken, alert='El Seguro del auto '+seguro.vehiculo.alias+' se encuentra activo', sound='default', action='verifica.Update', badge=True, push_time='now', vehiculo=seguro.vehiculo.id)
#             else:
#                 push.send_push(deviceToken=recibo.cotizacion.client.deviceToken, alert='La poliza '+recibo.poliza+' se encuentra activa', sound='default', badge=True, push_time='now')
            recibo.save()
            return Response({'status':'OK: Poliza activa'}, status=status.HTTP_200_OK)
        elif poliza_status == 'pendiente':
            recibo.cancelado = False
            if recibo.seguro:
            # Reestablece el seguro al vehiculo original
                seguro = recibo.seguro
                seguro.vehiculo = recibo.vehiculo
                seguro.activo = False
                seguro.aseguradora = recibo.cotizacion.aseguradora
                seguro.save()
                recibo.vehiculo = None
                recibo.seguro = None
#                 push.send_push(deviceToken=seguro.vehiculo.client.deviceToken, alert='El Seguro del auto '+seguro.vehiculo.alias+' se encuentra pendiente de pago', sound='default', action='verifica.Update', badge=True, push_time='now', vehiculo=seguro.vehiculo.id)
#             else:
#                 push.send_push(deviceToken=recibo.cotizacion.client.deviceToken, alert='La poliza '+recibo.poliza+' se encuentra pendiente de pago', sound='default', badge=True, push_time='now')
            recibo.save()
            return Response({'status':'OK: Poliza pendiente'}, status=status.HTTP_200_OK)

def parse_seguro(seguro=None, poliza_status='', motivo=None):
    client = seguro.vehiculo.client
#     if seguro.activo == True and poliza_status == 'cancelado':
#         return Response({'status':'Error: Poliza se encuentra activa'}, status=status.HTTP_400_BAD_REQUEST)
    if seguro.activo == True and poliza_status == 'activo':
        return Response({'status':'No hay cambios'}, status=status.HTTP_400_BAD_REQUEST)
    if seguro.activo == False and poliza_status == 'pendiente':
        return Response({'status':'No hay cambios'}, status=status.HTTP_400_BAD_REQUEST)
    if poliza_status == 'activo':
        push.send_push(deviceToken=client.deviceToken, alert='El Seguro del auto '+seguro.vehiculo.alias+' se encuentra activo', sound='default', action='verifica.Update', badge=True, push_time='now', vehiculo=seguro.vehiculo.id)
        seguro.activo = True
        seguro.save()
        return Response({'status':'OK: Poliza activada'}, status=status.HTTP_200_OK)
    elif poliza_status == 'pendiente':
        if motivo:
            push.send_push(deviceToken=client.deviceToken, alert='El Seguro del auto '+seguro.vehiculo.alias+' se encuentra pendiente. Motivo: '+motivo, sound='default', action='verifica.Update', badge=True, push_time='now', vehiculo=seguro.vehiculo.id)        
        else:
            push.send_push(deviceToken=client.deviceToken, alert='El Seguro del auto '+seguro.vehiculo.alias+' se encuentra pendiente hasta cubrir el pago correspondiente', sound='default', action='verifica.Update', badge=True, push_time='now', vehiculo=seguro.vehiculo.id)
        seguro.activo = False
        seguro.save()
        return Response({'status':'OK: Poliza desactivada'}, status=status.HTTP_200_OK)
    elif poliza_status == 'cancelado':
        if motivo:
            push.send_push(deviceToken=client.deviceToken, alert='El Seguro del auto '+seguro.vehiculo.alias+' ha sido cancelado. Motivo: '+motivo, sound='default', action='verifica.Update', badge=True, push_time='now', vehiculo=seguro.vehiculo.id)        
        else:
            push.send_push(deviceToken=client.deviceToken, alert='El Seguro del auto '+seguro.vehiculo.alias+' ha sido cancelado por falta de pago', sound='default', action='verifica.Update', badge=True, push_time='now', vehiculo=seguro.vehiculo.id)
        try:
            recibo = models.Recibo.objects.get(poliza=seguro.poliza)
        except:
            recibo = None
        parse_recibo(recibo=recibo, seguro=seguro, poliza_status=poliza_status)
        return Response({'status':'OK: Poliza cancelada'}, status=status.HTTP_200_OK)
    else:
        return Response({'status':'Error: Status incorrecto'}, status=status.HTTP_400_BAD_REQUEST)

class PolizaStatusView(APIView):
    model = models.Seguro
    queryset = models.Seguro.objects.all()
    permission_classes = (extra_permissions.AuthOnlyModelPermissions,)
    def post(self, request, format=None):
        serializer = serializers.InteresseSerializer(data=request.data)
        if serializer.is_valid():
            poliza_status = serializer.data['status']
            try:
                seguros = models.Seguro.objects.filter(poliza=serializer.data['poliza'])
            except:
                seguros = None
            if len(seguros) >= 1:
                for seguro in seguros:
                    if seguro.vehiculo:
                        try:
                            motivo = serializer.data['motivo']
                        except:
                            motivo = None
                        retVal = parse_seguro(seguro, poliza_status=poliza_status, motivo=motivo)                    
                    else:
                        try:
                            recibo = models.Recibo.objects.get(poliza=serializer.data['poliza'])
                        except:
                            recibo = None
                        if recibo:
                            retVal = parse_recibo(recibo, poliza_status=poliza_status)
                        else:
                            retVal = Response({'status':'Object Not Found'}, status=status.HTTP_400_BAD_REQUEST)                    
                return retVal
            else:
                try:
                    recibo = models.Recibo.objects.get(poliza=serializer.data['poliza'])
                except:
                    recibo = None
                if recibo:
                    return parse_recibo(recibo, poliza_status=poliza_status)
                else:
                    return Response({'status':'Object Not Found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
