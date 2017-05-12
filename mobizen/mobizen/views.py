# -*- coding: utf-8 -*- 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Avg, Q
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template import RequestContext

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
from rest_framework.reverse import reverse as rest_reverse

from django_modalview.generic.edit import ModalFormView, ModalUpdateView, ModalFormUtilView, ModalCreateView, ModalDeleteView
from django_modalview.generic.component import ModalResponse, ModalButton
from django_modalview.generic.base import ModalTemplateView, ModalTemplateUtilView

from drivemee import serializers
from drivemee import models
from drivemee import forms
from drivemee import utilities

from verifica.models import Client, Vehiculo, TipoPlaca
from verifica import push, verificador, slackbot, extra_permissions, placa_detector

import requests, json
import datetime
import locale

# Operador Modals
class OperadorDeleteModal(ModalDeleteView):
    def __init__(self, *args, **kwargs):
        super(OperadorDeleteModal, self).__init__(*args, **kwargs)
        self.title = "Eliminar Operador"
        self.submit_button.value = 'Eliminar'
        self.submit_button.type = 'danger'
        self.close_button.value = 'Cerrar'
        self.close_button.type = 'default'
    def dispatch(self, request, *args, **kwargs):
        self.object = models.Operador.objects.get(pk=kwargs.get('pk'))
        return super(OperadorDeleteModal, self).dispatch(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        super(OperadorDeleteModal, self).delete(request, *args, **kwargs)
        self.redirect_to = reverse('drivemee:operadores')
        messages.success(self.request, u'Se eliminó al operador')

class OperadorUpdateModal(ModalUpdateView):
    class Meta:
        model = models.Operador
    def __init__(self, *args, **kwargs):
        super(OperadorUpdateModal, self).__init__(*args, **kwargs)
        self.title = "Editar Datos del Operador"
        self.form_class = forms.OperadorCreateForm
        self.close_button.type = 'default'
        self.close_button.value = 'Cerrar'
        self.submit_button.value = 'Guardar'
    def form_valid(self, form, **kwargs):
        self.response = ModalResponse("Cambios guardados", "success")
        self.redirect_to = reverse('drivemee:operador-detail', args=(self.kwargs.get('pk'),))
        messages.info(self.request, 'Se modificaron los datos')
        return super(OperadorUpdateModal, self).form_valid(form, **kwargs)
    def dispatch(self, request, *args, **kwargs):
        self.object = models.Operador.objects.get(pk=kwargs.get('pk'))
        return super(OperadorUpdateModal, self).dispatch(request, *args, **kwargs)

class OperadorCreateModal(ModalCreateView):
    def __init__(self, *args, **kwargs):
        super(OperadorCreateModal, self).__init__(*args, **kwargs)
        self.title = "Nuevo Operador"
        self.form_class = forms.OperadorCreateForm
        self.close_button.value = 'Cerrar'
        self.close_button.type = 'default'
        self.submit_button.value = "Crear"
    def form_valid(self, form, **kwargs):
        self.redirect_to = reverse('drivemee:operadores')
        return super(OperadorCreateModal, self).form_valid(form, **kwargs)

# Operador Views
class OperadorListView(generic.ListView):
    template_name = 'drivemee/operadores-list.html'
    context_object_name = 'operadores_list'
    paginate_by = 50
    def get_queryset(self):
        return models.Operador.objects.all()
    def get_context_data(self, **kwargs):
        context = super(OperadorListView, self).get_context_data(**kwargs)
        context['title'] = 'Operadores'
        context['source'] = 'operadores'
        return context
    @method_decorator(login_required(login_url='/drivemee/login'))
    def dispatch(self, *args, **kwargs):
        return super(OperadorListView, self).dispatch(*args, **kwargs)

class OperadorDetailView(generic.DetailView):
    model = models.Operador
    template_name = 'drivemee/operador-detail.html'
    def get_context_data(self, **kwargs):
        context = super(OperadorDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Detalle'
        context['recent_evaluaciones_list'] = self.get_object().evaluaciones.filter(solicitud__operador=self.object)
        context['recent_solicitudes_list'] = self.get_object().solicitudes.filter(operador=self.object)
        activo_statuses = ('abierto','preagendado','agendado','verificado','proceso')
        context['active_solicitudes_list'] = self.get_object().solicitudes.filter(operador=self.object, status__in=activo_statuses)
        context['calificacion_operador'] = self.get_object().solicitudes.filter(operador=self.object, evaluacion__no_quiso_calificar=False).aggregate(Avg('evaluacion__calificacion'))
        return context
    @method_decorator(login_required(login_url='/drivemee/login'))
    def dispatch(self, *args, **kwargs):
        return super(OperadorDetailView, self).dispatch(*args, **kwargs)


# Solicitud Modals
class SolicitudRescheduleModal(ModalTemplateUtilView):
    def __init__(self, *args, **kwargs):
        super(SolicitudRescheduleModal, self).__init__(*args, **kwargs)
        self.title = u"Reagendar Solicitud"
        self.description = u"¿Estás seguro que deseas reagendar la solicitud?"
        self.close_button.value = 'Cancelar'
        self.close_button.type = 'default'
        self.util_button = ModalButton('Reagendar')
    def util(self, *args, **kwargs):
        if self.request.GET.get('util') == 'true':
            solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
            solicitud.status = 'reagendado'
            solicitud.timestamp_cerrado = timezone.now()
            solicitud.save()
            
            try:
                documentos = solicitud.documentos
            except:
                documentos = None
            direcciones = solicitud.direcciones.all()
            # duplicamos la solicitud
            solicitud.pk = None
            solicitud.timestamp_cerrado = None
            solicitud.timestamp_agendado = None
            solicitud.timestamp_proceso = None
            solicitud.status = 'abierto'
            solicitud.linked_solicitudes = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
            token = models.SolicitudInternal.objects.create()
            token.save()
            solicitud.solicitudToken = token
            solicitud.save()
            
            solicitud.documentos = models.Documento()
            if documentos:
                solicitud.documentos.seguro = documentos.seguro
                solicitud.documentos.adeudos = documentos.adeudos
                solicitud.documentos.tarjeta = documentos.tarjeta
                solicitud.documentos.certificado = documentos.certificado
                solicitud.documentos.enterado = documentos.enterado
                solicitud.documentos.save()
            else:
                solicitud.documentos.seguro = False
                solicitud.documentos.adeudos = False
                solicitud.documentos.tarjeta = False
                solicitud.documentos.certificado = False
                solicitud.documentos.enterado = True
                solicitud.documentos.save()
            solicitud.direcciones = direcciones
            solicitud.operador = None
            solicitud.save()
            
            cupon = models.Cupon()
            cupon.name = 'Rechazo'
            cupon.codigo = 'rechazo-'+solicitud.solicitudToken.deviceToken
            cupon.descuento = 50
            cupon.numero_usos = 1
            cupon.client = solicitud.client
            cupon.save()
            solicitud.cupon = cupon
            solicitud.save()
            
            msg = 'Se ha generado una nueva solicitud'
            if solicitud.vehiculo:
                msg = msg+u' para el auto '+solicitud.vehiculo.alias
            push.send_push(deviceToken=solicitud.client.deviceToken,
                            alert=msg,
                            badge=True,
                            sound=' ',
                            push_time='now',
                            action='verifica.showValet',
                            token=solicitud.solicitudToken.deviceToken)
            self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
            messages.success(self.request, u'Se generó una nueva solicitud')

class SolicitudNagModal(ModalTemplateUtilView):
    def __init__(self, *args, **kwargs):
        super(SolicitudNagModal, self).__init__(*args, **kwargs)
        self.title = u"Error"
        self.description = u"No es posible agendar una solicitud si no cuenta con domicilio"
        self.close_button = None
        self.util_button = ModalButton('Continuar')
        self.util_button.type = 'warning'
    def util(self, *args, **kwargs):
        self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
        messages.warning(self.request, u'No es posible agendar una solicitud si no cuenta con domicilio')

class SolicitudSelectOperadorModal(ModalFormView):
    class Meta:
        model = models.Operador
    def __init__(self, *args, **kwargs):
        super(SolicitudSelectOperadorModal, self).__init__(*args, **kwargs)
        self.title = u"Selecciona al Operador"
        self.form_class = forms.OperadorForm
        self.submit_button.value = "Guardar"
        self.close_button.value = 'Cerrar'
        self.close_button.type = 'default'
#     def dispatch(self, request, *args, **kwargs):
#         self.object = models.Solicitud.objects.get(pk=self.kwargs.get('pk')).operador
#         return super(SolicitudSelectOperadorModal, self).dispatch(request, *args, **kwargs)
    def form_valid(self, form, **kwargs):
        solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
        operador = models.Operador.objects.get(pk=self.request.POST.get('nombre'))
        solicitud.operador = operador
        solicitud.save()
        messages.success(self.request, u'Se actualizó el Operador')
        self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
        return super(SolicitudSelectOperadorModal, self).form_valid(form, **kwargs)

class SolicitudDomicilioCreateModal(ModalCreateView):
    class Meta:
        model = models.Direccion
    def __init__(self, *args, **kwargs):
        super(SolicitudDomicilioCreateModal, self).__init__(*args, **kwargs)
        self.title = u"Agregar Dirección"
        self.form_class = forms.DomicilioForm
        self.submit_button.value = "Guardar"
        self.close_button.value = 'Cerrar'
        self.close_button.type = 'default'
    def form_valid(self, form, **kwargs):
        self.save(form)
        solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
        if solicitud.direcciones.count() == 1 and solicitud.direcciones.all()[0].tipo == 'ambos':
            dir = solicitud.direcciones.all()[0]
            if self.object.tipo == 'entrega':
                dir.tipo = 'recoleccion'
                dir.save()
            elif self.object.tipo == 'recoleccion':
                dir.tipo = 'entrega'
                dir.save()
            elif self.object.tipo == 'ambos':
                dir.delete()
        self.object.solicitud = solicitud
        self.object.save()
        messages.success(self.request, u'Se guardó el domicilio')
        self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
        return super(SolicitudDomicilioCreateModal, self).form_valid(form, **kwargs)

class SolicitudDomicilioEditModal(ModalUpdateView):
    class Meta:
        model = models.Direccion
    def __init__(self, *args, **kwargs):
        super(SolicitudDomicilioEditModal, self).__init__(*args, **kwargs)
        self.title = u"Modificar Dirección"
        self.form_class = forms.DomicilioForm
        self.submit_button.value = "Guardar"
        self.close_button.value = 'Cerrar'
        self.close_button.type = 'default'
        self.description = u'Si editas la dirección se borrarán las coordenadas'
    def dispatch(self, request, *args, **kwargs):
        self.object = models.Direccion.objects.get(pk=self.kwargs.get('domicilio'))
        return super(SolicitudDomicilioEditModal, self).dispatch(request, *args, **kwargs)
    def form_valid(self, form, **kwargs):
        if self.object.tipo == 'ambos' and self.object.solicitud.direcciones.count()==2:
            for dir in self.object.solicitud.direcciones.all():
                if not dir.tipo == 'ambos':
                    dir.delete()
        if form.has_changed() and not self.request.POST.get('longitud') and not self.request.POST.get('latitud'):
            self.object.latitud = 0
            self.object.longitud = 0
            self.object.save()
        if self.object.solicitud.status == 'pendiente':
            self.object.solicitud.status = 'abierto'
            self.object.solicitud.timestamp_confirmacion = timezone.now()
            self.object.solicitud.save()
        messages.success(self.request, u'Se actualizó el domicilio')
        self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
        return super(SolicitudDomicilioEditModal, self).form_valid(form, **kwargs)

class SolicitudRetirarModal(ModalTemplateUtilView):
    def __init__(self, *args, **kwargs):
        super(SolicitudRetirarModal, self).__init__(*args, **kwargs)
        self.title = u"Retirar Solicitud"
        self.description = u"Al retirar la solicitud podrás volver a reagendar y cambiar de operador si es necesario"
        self.close_button.value = 'Cancelar'
        self.close_button.type = 'default'
        self.util_button = ModalButton('Retirar Solicitud')
    def util(self, *args, **kwargs):
        if self.request.GET.get('util') == 'true':
            solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
            solicitud.status = 'abierto'
            solicitud.timestamp_proceso = None
            solicitud.timestamp_agendado = None
            cita = solicitud.cita
            cita.delete()
            solicitud.save()
            self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
            messages.success(self.request, 'Solicitud Retirada')

class SolicitudIniciarModal(ModalTemplateUtilView):
    def __init__(self, *args, **kwargs):
        super(SolicitudIniciarModal, self).__init__(*args, **kwargs)
        self.title = u"Iniciar Proceso"
        self.description = u"Marcar la solicitudo como en Proceso"
        self.close_button.value = 'Cancelar'
        self.close_button.type = 'default'
        self.util_button = ModalButton('Iniciar Proceso')
    def util(self, *args, **kwargs):
        if self.request.GET.get('util') == 'true':
            solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
            solicitud.status = 'proceso'
            solicitud.timestamp_proceso = timezone.now()
            solicitud.save()
            msg = 'Servicio de Verificación en Proceso'
            push.send_push(deviceToken=solicitud.client.deviceToken,
                            alert=msg,
                            sound=' ',
                            push_time='now',
                            action='verifica.showValet',
                            token=solicitud.solicitudToken.deviceToken)
            self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
            messages.success(self.request, 'Solicitud Iniciada')

class SolicitudCloseModal(ModalTemplateUtilView):
    def __init__(self, *args, **kwargs):
        super(SolicitudCloseModal, self).__init__(*args, **kwargs)
        self.title = u"Cerrar Solicitud"
        self.description = u"¿Estás seguro que deseas cerrar la solicitud?"
#         self.form_class = forms.SolicitudVerificarForm
#         self.content_template_name = 'django_modalview/datepicker_modal.html'
#         self.submit_button.value = "Guardar"
        self.close_button.value = 'Cancelar'
        self.close_button.type = 'default'
        self.util_button = ModalButton('Cerrar Solicitud')
    def util(self, *args, **kwargs):
        if self.request.GET.get('util') == 'true':
            solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
            solicitud.status = 'cerrado'
            solicitud.timestamp_cerrado = timezone.now()
            solicitud.save()
            msg = 'Se ha concluido el servicio. Evalúanos para seguir mejorando'
            push.send_push(deviceToken=solicitud.client.deviceToken,
                            alert=msg,
                            badge=True,
                            sound=' ',
                            push_time='now',
                            action='verifica.showValet',
                            token=solicitud.solicitudToken.deviceToken)
            self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
            messages.success(self.request, 'Solicitud Cerrada')

class SolicitudVerificarModal(ModalFormView):
    def __init__(self, *args, **kwargs):
        super(SolicitudVerificarModal, self).__init__(*args, **kwargs)
        self.title = u"Resultado de Verificación"
        self.form_class = forms.SolicitudVerificarForm
        self.submit_button.value = "Guardar"
        self.close_button.value = 'Cerrar'
        self.close_button.type = 'default'
    def form_valid(self, form, **kwargs):
        holograma = self.request.POST.get('resultado')
        solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
        resultado = models.Resultado(resultado=holograma, solicitud=solicitud)
        resultado.save()
        solicitud.status = 'verificado'
        solicitud.save()
        try:
            vehiculo = solicitud.vehiculo
        except:
            vehiculo = None
        if vehiculo and holograma != 'RECHAZO':
            # calcular vigencia y guardar
            vigencia = verificador.vigencia_verificacion(vehiculo.placa, holograma)
            verificacion = vehiculo.verificacion.all()[0]
            verificacion.resultado = holograma
            verificacion.fecha = timezone.now()
            verificacion.vigencia = vigencia
            verificacion.manual = False
            verificacion.save()
        msg = u'Hemos verificado tu vehículo, ya se encuentra en camino a tu domicilio'
        push.send_push(deviceToken=solicitud.client.deviceToken,
                        alert=msg,
                        badge=True,
                        sound=' ',
                        push_time='now',
                        action='verifica.showValet',
                        token=solicitud.solicitudToken.deviceToken)
        self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
        messages.success(self.request, u'Verificación actualizada')
        return super(SolicitudVerificarModal, self).form_valid(form, **kwargs)

class SolicitudPreagendarModal(ModalFormView):
    def __init__(self, *args, **kwargs):
        super(SolicitudPreagendarModal, self).__init__(*args, **kwargs)
        self.title = "Escoge la fecha"
        self.description = "Preagendar Solicitud para la fecha indicada"
        self.form_class = forms.SolicitudPreagendarForm
        self.submit_button.value = "Confirmar"
        self.close_button.value = 'Cerrar'
        self.close_button.type = 'default'
    def form_valid(self, form, **kwargs):
        date = datetime.datetime.strptime(self.request.POST['fecha'], '%Y-%m-%d %H:%M')
        solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
        solicitud.snooze_until_date = date
        solicitud.status = 'preagendado'
        solicitud.save()
        razon = models.SnoozeReason()
        razon.solicitud = solicitud
        razon.snoozed_until_date = date
        razon.motivo = 'Preagendar'
        razon.save()
        self.redirect_to = reverse('drivemee:solicitudes', args=(self.kwargs.get('source'),self.kwargs.get('status')))
        messages.success(self.request, u'Solicitud preagendada para la fecha solicitada')
        return super(SolicitudPreagendarModal, self).form_valid(form, **kwargs)

class SolicitudNotesModal(ModalFormView):
    def __init__(self, *args, **kwargs):
        super(SolicitudNotesModal, self).__init__(*args, **kwargs)
        self.title = "Agregar Nota"
        self.description = ""
        self.form_class = forms.SolicitudNotesForm
        self.submit_button.value = "Guardar"
        self.close_button.value = 'Cancelar'
        self.close_button.type = 'default'
    def form_valid(self, form, **kwargs):
        solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
        nota = models.Note()
        nota.solicitud = solicitud
        nota.motivo = self.request.POST.get('motivo')
        nota.save()
        self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
        return super(SolicitudNotesModal, self).form_valid(form, **kwargs)

class SolicitudSnoozeModal(ModalFormView):
    def __init__(self, *args, **kwargs):
        super(SolicitudSnoozeModal, self).__init__(*args, **kwargs)
        self.title = "Escoge la fecha"
        self.description = "Posponer Solicitud hasta la fecha indicada"
        self.form_class = forms.SolicitudProcrastinateForm
        self.submit_button.value = "Confirmar"
        self.close_button.value = 'Cerrar'
        self.close_button.type = 'default'
    def form_valid(self, form, **kwargs):
        date = datetime.datetime.strptime(self.request.POST['fecha'], '%Y-%m-%d %H:%M')
        solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
        solicitud.snooze_until_date = date
        solicitud.save()
        
        razon = models.SnoozeReason()
        razon.solicitud = solicitud
        razon.snoozed_until_date = date
        razon.motivo = self.request.POST.get('motivo')
        razon.save()
#         locale.setlocale(locale.LC_ALL, "es_MX.UTF-8")
#         msg = 'Tu solicitud quedará pendiente hasta el {0:%A} {0:%d}'.format(date)
#         push.send_push(deviceToken=solicitud.client.deviceToken,
#                         alert=msg,
#                         badge=True,
#                         sound=' ',
#                         push_time='now',
#                         action='verifica.showValet',
#                         token=solicitud.solicitudToken.deviceToken)
        self.redirect_to = reverse('drivemee:solicitudes', args=(self.kwargs.get('source'),self.kwargs.get('status')))
        messages.success(self.request, u'Solicitud silenciada hasta la fecha solicitada')
        return super(SolicitudSnoozeModal, self).form_valid(form, **kwargs)

class SolicitudScheduleModal(ModalFormView):
    def __init__(self, *args, **kwargs):
        super(SolicitudScheduleModal, self).__init__(*args, **kwargs)
        self.title = "Escoge la fecha"
        self.form_class = forms.SolicitudScheduleForm
        self.submit_button.value = "Agendar"
        self.close_button.value = 'Cerrar'
        self.close_button.type = 'default'
    def form_valid(self, form, **kwargs):
        print(self.request.POST['fecha'])
        date = datetime.datetime.strptime(self.request.POST['fecha'], '%Y-%m-%d %H:%M')
        solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
        try:
            cita = solicitud.cita
        except:
            cita = models.Cita(solicitud=solicitud, fecha=date)
        cita.fecha = date
        cita.save()
        if not solicitud.vehiculo:
            """Intenta buscar el vehiculo del usuario en caso de que no se haya ligado a la solicitud correctamente"""
            for tmp_vehiculo in solicitud.client.vehiculos.all():
                if tmp_vehiculo.placa == solicitud.placa:
                    solicitud.vehiculo = tmp_vehiculo
                    solicitud.save()
                    break
        try:
            vehiculo = solicitud.vehiculo.alias
        except:
            vehiculo = solicitud.placa
        # Guarda el costo real de la solicitud tomando en cuenta el estado de la placa y si hay cupones
        is_tarde = verificador.is_ultima_semana_periodo(date)
        # workaround temporal para la semana de prorroga en septiembre 2016
        if date.month == 9:
            if date.day >= 12 and date.day <= 15:
                ultimo_digito = verificador.ultimo_digito(solicitud.placa)
                if ultimo_digito == 5 or ultimo_digito == 6:
                    is_tarde = True
        tipo_placa = placa_detector.parse_placa(solicitud.placa)
        tipo_tarifa = 'tarde' if is_tarde==True else 'normal'
        try: 
            tarifa = models.Tarifa.objects.get(estado=tipo_placa.estado, tipo=tipo_tarifa)
        except:
            tarifa = models.Tarifa.objects.get(estado='DIF', tipo=tipo_tarifa)
        costo = tarifa.costo
        if solicitud.cupon:
            costo = (costo * (100-solicitud.cupon.descuento))/100
        solicitud.costo_real = costo
        solicitud.save()
        locale.setlocale(locale.LC_ALL, "es_MX.UTF-8")
        fecha = 'La cita es el {0:%A} {0:%d}, a las {0:%H:%M} hrs'.format(cita.fecha)
        if solicitud.status == 'abierto' or solicitud.status == 'preagendado':
            solicitud.status = 'agendado'
            solicitud.timestamp_agendado = timezone.now()
            solicitud.snooze_until_date = None
            solicitud.save()
            msg = 'Se agendó el Servicio de Valet para el auto {0}. {1}'.format(vehiculo,fecha)
        else:
            msg = 'Se reagendó el Servicio de Valet para el auto {0}. {1}'.format(vehiculo,fecha)
        push.send_push(deviceToken=solicitud.client.deviceToken,
                        alert=msg,
                        badge=True,
                        sound=' ',
                        push_time='now',
                        action='verifica.showValet',
                        token=solicitud.solicitudToken.deviceToken)
        self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
        messages.success(self.request, u'Se agendó correctamente')
        return super(SolicitudScheduleModal, self).form_valid(form, **kwargs)

class SolicitudCreateModal(ModalCreateView):
    def __init__(self, *args, **kwargs):
        super(SolicitudCreateModal, self).__init__(*args, **kwargs)
        self.title = "Nueva Solicitud"
        self.form_class = forms.SolicitudCreateForm
        self.close_button.value = 'Cerrar'
        self.close_button.type = 'default'
    def form_valid(self, form, **kwargs):
        self.response = ModalResponse("Solicitud Creada", "success")
        return super(SolicitudCreateModal, self).form_valid(form, **kwargs)

class SolicitudCancelModal(ModalFormView):
    def __init__(self, *args, **kwargs):
        super(SolicitudCancelModal, self).__init__(*args, **kwargs)
        self.title = "Cancelar Solicitud"
        self.form_class = forms.CancelForm
        self.submit_button.value = 'Cancelar'
        self.submit_button.type = 'danger'
        self.close_button.value = 'Cerrar'
        self.close_button.type = 'default'
    def form_valid(self, form, **kwargs):
        status = self.request.POST.get('status')
        motivo = self.request.POST.get('motivo')
        solicitud = models.Solicitud.objects.get(pk=self.kwargs.get('pk'))
        solicitud.timestamp_cerrado = timezone.now()
        solicitud.status = status
        solicitud.save()
        reporte = models.Reporte(solicitud=solicitud, motivo=motivo)
        reporte.save()
        if status == 'cancelado':            
            msg = u'Se canceló la solicitud de Verificación a Domicilio'
            push.send_push(deviceToken=solicitud.client.deviceToken,
                            alert=msg,
                            badge=True,
                            sound=' ',
                            push_time='now',
                            action='verifica.showValet',
                            token=solicitud.solicitudToken.deviceToken)
        self.redirect_to = reverse('drivemee:solicitudes', args=(self.kwargs.get('source'),self.kwargs.get('status')))
        messages.success(self.request, u'Solicitud Cancelada')
        return super(SolicitudCancelModal, self).form_valid(form, **kwargs)
    def dispatch(self, request, *args, **kwargs):
        self.object = models.Solicitud.objects.get(pk=kwargs.get('pk'))
        return super(SolicitudCancelModal, self).dispatch(request, *args, **kwargs)

class SolicitudClientUpdateModal(ModalUpdateView):
    class Meta:
        model = models.Solicitud
    def __init__(self, *args, **kwargs):
        super(SolicitudClientUpdateModal, self).__init__(*args, **kwargs)
        self.title = "Editar Datos de Contacto"
        self.form_class = forms.DatosClienteForm
        self.close_button.type = 'default'
        self.close_button.value = 'Cerrar'
        self.submit_button.value = 'Guardar'
    def form_valid(self, form, **kwargs):
        self.save(form)
        if self.object.status == 'pendiente':
            self.object.status = 'abierto'
            self.object.timestamp_confirmacion = timezone.now()
            self.object.save()
        self.response = ModalResponse("Cambios guardados", "success")
        self.redirect_to = reverse('drivemee:solicitud-detail', args=(self.kwargs.get('source'),self.kwargs.get('status'),self.kwargs.get('pk')))
        messages.info(self.request, 'Se modificaron los datos')
        return super(SolicitudClientUpdateModal, self).form_valid(form, **kwargs)
    def dispatch(self, request, *args, **kwargs):
        self.object = models.Solicitud.objects.get(pk=kwargs.get('pk'))
        return super(SolicitudClientUpdateModal, self).dispatch(request, *args, **kwargs)

def SolicitudSearchView(request):
    if request.method == 'GET': # If the form is submitted
        search_query = request.GET.get('term', None)
        is_placa = False
        try:
            search_query = int(search_query)
        except:
            is_placa = True
            search_query = search_query.upper()
        if is_placa:
            try:
                solicitud = models.Solicitud.objects.get(placa=search_query)
            except:
                solicitud = None
        else:
            try:
                solicitud = models.Solicitud.objects.get(folio=search_query-10000321)
            except:
                solicitud = None
        if solicitud:
        #warn
            return HttpResponseRedirect(reverse('drivemee:solicitud-detail', args=(solicitud.folio,)))
        else:
            return HttpResponseRedirect(reverse('drivemee:solicitudes')+'?busqueda='+search_query)

def logout(request):
    return auth_logout(request, next_page='drivemee:index', template_name='registration/logout.html')

def index(request):
    context = {'title':'DriveMee'}
    context['tarifas'] = models.Tarifa.objects.all().order_by('estado', 'tipo')
    return render(request, 'drivemee/index.html', context)
#     return HttpResponseRedirect(reverse('drivemee:solicitudes'))

class SolicitudIndexView(generic.ListView):
    template_name = 'drivemee/list.html'
    context_object_name = 'latest_solicitud_list'
    paginate_by = 25
    def get_queryset(self):
        if self.request.GET.get('busqueda'):
            try:
                return models.Solicitud.objects.filter(placa=self.request.GET.get('busqueda')).order_by('-timestamp_confirmacion', '-timestamp_abierto')
            except:
                return None
        else:
            source = self.kwargs.get('source')
            status = self.kwargs.get('status')
            invalid_clients = ['admin','web','drivemee','verifica']
            if source == 'agencia':
                source_query = Q(client__deviceToken__in=invalid_clients)
            else:
                source_query = ~Q(client__deviceToken__in=invalid_clients)
            today = datetime.datetime.today()
            if status == 'pospuesta':
                return models.Solicitud.objects.filter(Q(snooze_until_date__gte=today) & ~Q(status=status) & source_query).order_by('snooze_until_date','timestamp_confirmacion', 'timestamp_abierto')
            if status == 'cancelado':
                cancelado_statuses = ('no_contratado','cancelado','caido')
                return models.Solicitud.objects.filter(Q(status__in=cancelado_statuses) & source_query).order_by('-timestamp_cerrado')[:250]
            elif status == 'proceso':
                proceso_statuses = ('verificado','proceso')
                return models.Solicitud.objects.filter(Q(status__in=proceso_statuses) & source_query).filter(Q(snooze_until_date__lte=today)|Q(snooze_until_date=None)).order_by('-timestamp_proceso')
            elif status == 'cerrado':
                cerrado_statuses = ('cerrado', 'reagendado')
                return models.Solicitud.objects.filter(Q(status__in=cerrado_statuses) & source_query).order_by('-timestamp_cerrado','cita__fecha','timestamp_confirmacion', 'timestamp_abierto')[:400]
            if status == 'activo':
                activo_statuses = ('abierto','preagendado','agendado','verificado','proceso')
                return models.Solicitud.objects.filter(status__in=activo_statuses).filter(source_query&(Q(cita__fecha__lte=timezone.now()+datetime.timedelta(days=21))|Q(cita=None)|Q(cita__fecha=None))&(((Q(snooze_until_date__lte=today)|Q(snooze_until_date=None))&~Q(status='preagendado'))|(Q(status='preagendado')&Q(snooze_until_date__lte=today+datetime.timedelta(days=21))))).order_by('-timestamp_confirmacion', '-timestamp_abierto', '-timestamp_agendado', '-timestamp_proceso',)
            else:
                return models.Solicitud.objects.filter(status=status).filter(source_query&(Q(cita__fecha__lte=timezone.now()+datetime.timedelta(days=21))|Q(cita=None)|Q(cita__fecha=None))&(((Q(snooze_until_date__lte=today)|Q(snooze_until_date=None))&~Q(status='preagendado'))|(Q(status='preagendado')&Q(snooze_until_date__lte=today+datetime.timedelta(days=21))))).order_by('-timestamp_cerrado','cita__fecha','snooze_until_date','timestamp_confirmacion', 'timestamp_abierto')

    def get_context_data(self, **kwargs):
        source = self.kwargs.get('source')
        status = self.kwargs.get('status')
        context = super(SolicitudIndexView, self).get_context_data(**kwargs)
        context['title'] = 'Solicitudes '+source
        context['current_list'] = 'solicitudes'
        context['source'] = source
        context['status'] = status
        context['selected_status'] = status
        if self.request.GET.get('busqueda'):
            context['from_search'] = True
            context['selected_status'] = 'search'
        today = datetime.datetime.today()
        invalid_clients = ['admin','web','drivemee','verifica']
        if source == 'agencia':
            source_query = Q(client__deviceToken__in=invalid_clients)
        else:
            source_query = ~Q(client__deviceToken__in=invalid_clients)
        activo_statuses = ('abierto','preagendado','agendado','verificado','proceso')
        context['count_activo'] = models.Solicitud.objects.filter(status__in=activo_statuses).filter(source_query&(Q(cita__fecha__lte=timezone.now()+datetime.timedelta(days=21))|Q(cita=None)|Q(cita__fecha=None))&(((Q(snooze_until_date__lte=today)|Q(snooze_until_date=None))&~Q(status='preagendado'))|(Q(status='preagendado')&Q(snooze_until_date__lte=today+datetime.timedelta(days=21))))).count()
        context['count_abierto'] = models.Solicitud.objects.filter(Q(status='abierto')&source_query).filter(Q(snooze_until_date__lte=today)|Q(snooze_until_date=None)).count()
        context['count_preagendado'] = models.Solicitud.objects.filter(Q(status='preagendado')&source_query).filter(Q(snooze_until_date__lte=timezone.now()+datetime.timedelta(days=21))).count()
        context['count_agendado'] = models.Solicitud.objects.filter(Q(status='agendado')&source_query).filter(Q(cita__fecha__lte=timezone.now()+datetime.timedelta(days=21))).count()
        proceso_statuses = ('verificado','proceso')
        context['count_proceso'] = models.Solicitud.objects.filter(Q(status__in=proceso_statuses)&source_query).filter(Q(snooze_until_date__lte=today)|Q(snooze_until_date=None)).count()
        if source == 'cerrado':
            context['count_cerrado'] = models.Solicitud.objects.filter((Q(status='cerrado')|Q(status='reagendado'))&source_query).count()
        if source == 'cancelado':
            cancelado_statuses = ('no_contratado','cancelado','caido')
            context['count_cancelado'] = models.Solicitud.objects.filter(Q(status__in=cancelado_statuses)&source_query).count()
        if source == 'pospuesta':
            cancelado_statuses = ('no_contratado','cancelado','caido')
            context['count_pospuesta'] = models.Solicitud.objects.filter(Q(snooze_until_date__gte=today)&source_query).count()
        return context
    @method_decorator(login_required(login_url='/drivemee/login'))
    def dispatch(self, *args, **kwargs):
        return super(SolicitudIndexView, self).dispatch(*args, **kwargs)

class SolicitudDetailView(generic.DetailView):
    model = models.Solicitud
    template_name = 'drivemee/detail.html'
#     def get_object(self):
#         queryset = models.Solicitud.objects.all()
#         object = get_object_or_404(queryset, folio=int(self.kwargs.get('pk'))-10000321)
#         return object
    def get_context_data(self, **kwargs):
        context = super(SolicitudDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Detalle'
        context['direcciones_list'] = self.get_object().direcciones.all()        
        context['source'] = self.kwargs.get('source')
        context['status'] = self.kwargs.get('status')
        source = self.kwargs.get('source')
        status = self.kwargs.get('status')
        ultimo_digito = verificador.ultimo_digito(self.get_object().placa)
        if self.get_object().status == 'abierto' or self.get_object().status == 'preagendado':
            now = timezone.now()
            context['meses_list'] = verificador.meses_puede_verificar(ultimo_digito)
            context['extemporaneo'] = verificador.is_placa_extemporaneo(self.get_object().placa)
            if verificador.is_periodo_started(self.get_object().placa,now):
                context['is_late'] = verificador.is_ultima_semana_periodo(now)
            if self.get_object().snooze_until_date and self.get_object().status != 'preagendado':
                context['is_snoozed'] = self.get_object().snooze_until_date >= now
        if not self.get_object().costo_real and self.get_object().status == 'abierto':            
            tipo_placa = placa_detector.parse_placa(self.get_object().placa)
            tarifas = models.Tarifa.objects.filter(estado=tipo_placa.estado).order_by('tipo')
            if verificador.is_periodo_started(self.get_object().placa,now):
                is_late = verificador.is_ultima_semana_periodo(timezone.now())
                if is_late:
                    tarifas = models.Tarifa.objects.filter(estado=tipo_placa.estado, tipo='tarde').order_by('tipo')
            precios = []
            if self.get_object().cupon:
                for tarifa in tarifas:
                    precios.append({'tipo':tarifa.tipo,
                                'precio':(tarifa.costo*(100-self.get_object().cupon.descuento))/100})
            else:
                for tarifa in tarifas:
                    precios.append({'tipo':tarifa.tipo,
                                'precio':tarifa.costo})
            context['precios_verificacion'] = precios
        return context
    @method_decorator(login_required(login_url='/drivemee/login'))
    def dispatch(self, *args, **kwargs):
        return super(SolicitudDetailView, self).dispatch(*args, **kwargs)




# API Views
class EvaluacionesView(APIView):
    """
    Da una lista con las evaluaciones pendientes.
    Indica el estatus de la solicitud para poder mostrar el formulario adecuado
    """
    queryset = models.Evaluacion.objects.all()
    permission_classes = (extra_permissions.AuthOnlyModelPermissions,)
    def get(self, request, format=None):
        params = request.GET
        client = None
        if 'deviceToken' in params:
            try:
                client = Client.objects.get(deviceToken=params['deviceToken'])
            except ObjectDoesNotExist:
                return Response({'status':'client not found'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':'Missing Device Token'},
                    status=status.HTTP_400_BAD_REQUEST)
        valid_statuses = ('cerrado','caido','cancelado','no_contratado')
        solicitudes = models.Solicitud.objects.filter(client=client, status__in=valid_statuses, evaluacion=None)
        serializer = serializers.EvaluacionListSerializer(solicitudes, many=True)
        return Response(serializer.data)

class CuponesAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Cupon.objects.all()
    serializer_class = serializers.CuponSerializer
#     permission_classes = (extra_permissions.AuthOnlyModelPermissions,)
    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def retrieve(self, request, pk=None):
        queryset = models.Cupon.objects.all()
        cupon = get_object_or_404(queryset, codigo=pk.upper())
        if cupon:
            params = request.GET
            client = None
            if 'deviceToken' in params:
                try:
                    client = Client.objects.get(deviceToken=params['deviceToken'])
                except ObjectDoesNotExist:
                    return Response({'status':'client not found'},
                                    status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'status':'Por favor actualiza la app para usar este cupón'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#             if 'tipo' in params:
#                 if not cupon.tipo == params.get('tipo'):
#                     return Response({'status':'Cupón no válido para este tipo de servicio'},
#                                     status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'status':'Por favor actualiza la app para usar este cupón'},
#                                 status=status.HTTP_400_BAD_REQUEST)
            if not cupon.activo:
                return Response({'status':'Cupón no disponible'})
            if cupon.client and cupon.client != client:
                    return Response({'status':'No tienes permiso de usar este cupón'})
            if cupon.numero_usos > 0:
                solicitudes = models.Solicitud.objects.filter(cupon=cupon)
                if len(solicitudes) >= cupon.numero_usos:
                    return Response({'status':'Cupón ha excedido número de usos'})
            if not cupon.permanente and cupon.vigencia and cupon.vigencia <= timezone.now():
                return Response({'status':'Este cupón ha expirado'})
        serializer = serializers.CuponSerializer(cupon)
        return Response(serializer.data)

class TarifasAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Tarifa.objects.all()
    serializer_class = serializers.TarifaSerializer
    permission_classes = (extra_permissions.AuthOnlyModelPermissions,)
    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SolicitudAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Solicitud.objects.all()
    serializer_class = serializers.SolicitudSerializer
    permission_classes = (extra_permissions.AuthOnlyModelPermissions,)
    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def list(self, request):
        params = request.GET
        client = None
        vehiculo = None
        if 'deviceToken' in params:
            try:
                client = Client.objects.get(deviceToken=params['deviceToken'])
            except ObjectDoesNotExist:
                return Response({'status':'client not found'},
                                status=status.HTTP_400_BAD_REQUEST)
        if 'vehiculo' in params:
            try:
                vehiculo = Vehiculo.objects.get(id=params['vehiculo'])
            except ObjectDoesNotExist:
                return Response({'status':'Vehiculo not found'},
                                status=status.HTTP_400_BAD_REQUEST)
            if vehiculo.client != client:
                return Response({'status':'Vehiculo no pertenece a Client'},
                                status=status.HTTP_400_BAD_REQUEST)
        if not client:
            return Response({'status':'Missing Device Token'},
                            status=status.HTTP_400_BAD_REQUEST)
        valid_statuses = ('abierto','agendado','preagendado','proceso','verificado', 'cerrado')
        if vehiculo:
            solicitudes = models.Solicitud.objects.all().filter(client=client, vehiculo=vehiculo, status__in=valid_statuses, evaluacion=None)
        else:
            solicitudes = models.Solicitud.objects.all().filter(client=client, status__in=valid_statuses, evaluacion=None)
        serializer = serializers.SolicitudSerializer(solicitudes, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = models.Solicitud.objects.all()
        params = request.GET
        client = None
        if 'deviceToken' in params:
            try:
                client = Client.objects.get(deviceToken=params['deviceToken'])
            except ObjectDoesNotExist:
                return Response({'status':'client not found'},
                                status=status.HTTP_400_BAD_REQUEST)
        if not client:
            return Response({'status':'Missing Device Token'},
                            status=status.HTTP_400_BAD_REQUEST)
        solicitud = get_object_or_404(queryset, solicitudToken=pk)
        if solicitud.client != client:
            return Response({'status':'Solicitud no pertenece a Client'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.SolicitudSerializer(solicitud)
        return Response(serializer.data)
    def create(self, request, pk=None):
        serializer = serializers.SolicitudInsertSerializer(data=request.data)
        if serializer.is_valid():
            try:
                owner = Client.objects.get(deviceToken=serializer.data['deviceToken'])
            except ObjectDoesNotExist:
                return Response({'status':'client not found'},
                                status=status.HTTP_400_BAD_REQUEST)
            if owner:
                invalid_statuses = ('abierto','agendado','proceso','verificado')
                solicitudes = models.Solicitud.objects.all().filter(placa=serializer.data['placa'], status__in=invalid_statuses, client=owner)
                if len(solicitudes) > 0:
                    return Response({'status':'Esta Placa ya tiene una solicitud abierta'},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    vehiculo = None
                    if 'vehiculo_id' in serializer.data:
                        try:
                            vehiculo = Vehiculo.objects.get(id=serializer.data['vehiculo_id'])
                        except ObjectDoesNotExist:
                            return Response({'status':'Vehiculo not found'},
                                            status=status.HTTP_400_BAD_REQUEST)
                        if vehiculo.client != owner:
                            return Response({'status':'Vehiculo no pertenece a Client'},
                                            status=status.HTTP_400_BAD_REQUEST)
                    cupon = None
                    if 'cupon' in serializer.data:
                        try:
                            cupon = models.Cupon.objects.get(codigo=serializer.data['cupon'].upper())
                        except ObjectDoesNotExist:
                            return Response({'status':'cupon not found'},
                                            status=status.HTTP_400_BAD_REQUEST)
                    placa_limpia = serializer.data['placa'].replace(' ','').replace('-','')
                    solicitud = models.Solicitud(nombre=serializer.data['nombre'],
                                                 email=serializer.data['email'],
                                                 telefono=serializer.data['telefono'],
                                                 placa=placa_limpia,
                                                 marca=serializer.data['marca'],
                                                 submarca=serializer.data['submarca'],
                                                 modelo=serializer.data['modelo'],
                                                 ultimo_holograma=serializer.data['ultimo_holograma'],
                                                 client=owner)
                    if vehiculo:
                        solicitud.vehiculo = vehiculo
                    if cupon:
                        solicitud.cupon = cupon
                    solicitud.save()
                    solicitud.timestamp_confirmacion = timezone.now()
                    solicitud.save()
#                     url = 'https://app.verifica.mx/drivemee/solicitud/'+str(solicitud.folio)+'/'
                    url = rest_reverse('drivemee:solicitud-detail', args=('app', 'activo', solicitud.folio), request=request)
                    utilities.send_lead_email(solicitud, request)
                    slackbot.send_message('Nuevo lead: '+url, channel='#leadsvalet')
                    return Response({'solicitudToken': solicitud.solicitudToken.deviceToken})
            else:
                return Response({'status':'client not found'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    # For POST Requests
    @detail_route(methods=['post'], permission_classes=[extra_permissions.AuthOnlyModelPermissions])
    def save_direccion(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.DireccionSerializer(data=request.data)
        queryset = models.Solicitud.objects.all()
        solicitud = get_object_or_404(queryset, solicitudToken=pk)
        if serializer.is_valid():
            try:
                owner = Client.objects.get(deviceToken=serializer.data['deviceToken'])
            except ObjectDoesNotExist:
                return Response({'status':'client not found'},
                                status=status.HTTP_400_BAD_REQUEST)
            if solicitud.client == owner:
                tipo = serializer.data['tipo']
                if tipo not in ('ambos', 'entrega', 'recoleccion'):
                    return Response({'status':'Tipo Incorrecto: Valores posibles: \'ambos\', \'entrega\', \'recoleccion\''},
                                    status=status.HTTP_400_BAD_REQUEST)
                if not {'calle', 'numero_exterior', 'colonia', 'estado', 'municipio', 'codigo_postal'}.issubset(serializer.data) and not {'latitud', 'longitud'}.issubset(serializer.data):
                    return Response({'status':'Faltan datos en la dirección'},
                                    status=status.HTTP_400_BAD_REQUEST)
                direccion = None
                if tipo == 'ambos':
                    solicitud.direcciones.all().delete()
                if len(solicitud.direcciones.all()):
                    for dir in solicitud.direcciones.all():
                        if dir.tipo == tipo:
                            direccion = dir
                if not direccion:
                    direccion = models.Direccion()
                direccion.tipo = serializer.data['tipo']
                direccion.solicitud = solicitud
                direccion.estado = serializer.data['estado']
                if 'calle' in serializer.data:
                    direccion.calle = serializer.data['calle']
                if 'numero_exterior' in serializer.data:
                    direccion.numero_exterior = serializer.data['numero_exterior']
                if 'numero_interior' in serializer.data:
                    direccion.numero_interior = serializer.data['numero_interior']
                if 'colonia' in serializer.data:
                    direccion.colonia = serializer.data['colonia']
                if 'municipio' in serializer.data:
                    direccion.municipio = serializer.data['municipio']
                if 'codigo_postal' in serializer.data:
                    direccion.codigo_postal = serializer.data['codigo_postal']
                if 'latitud' in serializer.data:
                    direccion.latitud = serializer.data['latitud']
                if 'longitud' in serializer.data:
                    direccion.longitud = serializer.data['longitud']
                if 'referencias' in serializer.data:
                    direccion.referencias = serializer.data['referencias']
                direccion.save()
                return Response({'status': 'direccion saved'})
            else:
                return Response({'status':'Solicitud no pertenece a Cliente'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @detail_route(methods=['post'], permission_classes=[extra_permissions.AuthOnlyModelPermissions])
    def save_documentos(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.DocumentosSerializer(data=request.data)
        queryset = models.Solicitud.objects.all()
        solicitud = get_object_or_404(queryset, solicitudToken=pk)
        if serializer.is_valid():
            try:
                owner = Client.objects.get(deviceToken=serializer.data['deviceToken'])
            except ObjectDoesNotExist:
                return Response({'status':'client not found'},
                                status=status.HTTP_400_BAD_REQUEST)
            if solicitud.client.deviceToken == serializer.data['deviceToken']:
                try:
                    documentos = solicitud.documentos
                except:
                    solicitud.documentos = models.Documento()
                solicitud.documentos.seguro = serializer.data['seguro']
                solicitud.documentos.adeudos = serializer.data['adeudos']
                solicitud.documentos.tarjeta = serializer.data['tarjeta']
                solicitud.documentos.certificado = serializer.data['certificado']
                solicitud.documentos.enterado = serializer.data['enterado']
                solicitud.documentos.save()
                return Response({'status': 'documentos saved'})
            else:
                return Response({'status':'Solicitud no pertenece a Cliente'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @detail_route(methods=['post'], permission_classes=[extra_permissions.AuthOnlyModelPermissions])
    def log_calificacion(self, request, pk=None):
        """ Updates the object identified by the pk """
        serializer = serializers.EvaluacionSerializer(data=request.data)
        if serializer.is_valid():
            queryset = models.Solicitud.objects.all()
            solicitud = get_object_or_404(queryset, solicitudToken=pk)
            try:
                owner = Client.objects.get(deviceToken=serializer.data['deviceToken'])
            except ObjectDoesNotExist:
                return Response({'status':'client not found'},
                                status=status.HTTP_400_BAD_REQUEST)
            if solicitud.client == owner:
                try:
                    evaluacion = solicitud.evaluacion
                except:
                    evaluacion = models.Evaluacion()
                evaluacion.operador = solicitud.operador
                if 'no_quiso_calificar' in serializer.data:
                    evaluacion.no_quiso_calificar = serializer.data['no_quiso_calificar']
                if 'calificacion' in serializer.data:
                    evaluacion.calificacion = serializer.data['calificacion']
                if 'comentarios' in serializer.data:
                    evaluacion.comentarios = serializer.data['comentarios']
                evaluacion.solicitud = solicitud
                evaluacion.save()
                return Response({'status': 'evaluacion saved'})
            else :
                return Response({'status':'Solicitud no pertenece a Cliente'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
