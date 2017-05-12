# -*- coding: utf-8 -*- 
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from drivemee import utilities
from drivemee import models
from drivemee import forms
from verifica.models import Client
from verifica import slackbot
from rest_framework.reverse import reverse as rest_reverse

# Nueva Solicitud desde DriveMee/Verifica

def aviso_privacidad(request):
    context = {'title':'Aviso de Privacidad'}
    return render(request, 'drivemee/drivemee-aviso-privacidad.html', context)

def thanks_solicitud(request, template=None, source='drivemee', **kwargs):
    if not template:
        template = 'drivemee/drivemee-submit-form.html'
    context = {}
    token = urlsafe_base64_decode(kwargs.get('token')).split('&')
    folio = token[0].split('=')[1]
    timestamp = utilities.date_from_unix_time(token[1].split('=')[1])
    context['folio'] = folio
#     return render(request, template, context)
    try:
        client, created = models.Client.objects.get_or_create(deviceToken=source)
        solicitud = models.Solicitud.objects.get(folio=int(folio)-10000321, client=client, status='pendiente')
    except:
        return HttpResponseRedirect(reverse('drivemee:index'))
    naive = timezone.make_naive(solicitud.timestamp_abierto, timezone.utc)
    if naive == timestamp:
        context['email'] = solicitud.email
        return render(request, template, context)
    else:
        return HttpResponseRedirect(reverse('drivemee:index'))

def thanks_solicitud_verifica(request, **kwargs):
    return thanks_solicitud(request, template='drivemee/verifica_submit_form.html', source='verifica', **kwargs)

def confirm_solicitud(request, token, template=None, source=None):
    encoded_string = urlsafe_base64_decode(token)
    folio = encoded_string.split('=')[1]
    context = {}
    try:
        clients = ['verifica', 'drivemee']
        solicitud = models.Solicitud.objects.get(folio=folio, status='pendiente', client__deviceToken__in=clients)
#         solicitud = models.Solicitud.objects.get(folio=folio, client__deviceToken__in=clients)
    except:
        return HttpResponseRedirect(reverse('drivemee:index'))
    if solicitud.client.deviceToken == 'verifica':
        source = 'app'
        template='drivemee/verifica_confirm_solicitud.html'
    elif solicitud.client.deviceToken == 'drivemee':
        source = 'agencia'
        template='drivemee/drivemee-confirm-solicitud.html'    
    solicitud.status = 'abierto'
    solicitud.timestamp_confirmacion = timezone.now()
    solicitud.save()
    context['source'] = source
    context['folio'] = solicitud.internal_folio()
    url = rest_reverse('drivemee:solicitud-detail', args=(source, 'activo', solicitud.folio), request=request)
#     utilities.send_lead_email(solicitud, request)
    slackbot.send_message('Nuevo lead: '+url, channel='#leadsvalet')
    return render(request, template, context)

def confirm_solicitud_verifica(request, token):
    return confirm_solicitud(request, token, template='drivemee/verifica_confirm_solicitud.html', source='verifica')

def create_solicitud(request, template=None, source=None):
    if not template:
        template = 'drivemee/drivemee-create-form.html'
    context = {}
    context['tarifas'] = models.Tarifa.objects.all().order_by('estado', 'tipo')
    context['cupones_api_url'] = rest_reverse('drivemee:cupon-list', request=request)
    if not source:
        target = 'drivemee:confirmar-solicitud'
        source = 'drivemee'
        context['solicitud_form_target'] = rest_reverse('drivemee:crear-solicitud', request=request)
    else:
        target = 'drivemee:verifica-confirmar-solicitud'
        context['solicitud_form_target'] = rest_reverse('drivemee:verifica-crear-solicitud', request=request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.PublicCreateSolicitudForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            client, created = Client.objects.get_or_create(deviceToken=source)
            try:
                statuses = ['abierto', 'agendado', 'proceso', 'verificado', 'pendiente']
                solicitud_repetida = models.Solicitud.objects.get(client=client, placa=form.cleaned_data['placa'], email=form.cleaned_data['email'], status__in=statuses)
            except MultipleObjectsReturned:
                solicitud_repetida = True
            except:
                solicitud_repetida = None
            if solicitud_repetida is not None:
                form.add_error(None,u'Esta placa ya tiene una solicitud abierta')
                context['form'] = form
                return render(request, template, context)

            if 'cupon' in form.data and form.data['cupon'] != '' and form.data['cupon'] != None:
                try:
                    cupon = models.Cupon.objects.get(codigo=form.cleaned_data['cupon'].upper())
                except:
                    form.add_error('cupon',u'Cupón inválido')
                    context['form'] = form
                    return render(request, template, context)
            else:
                cupon = None
            solicitud = models.Solicitud()
            solicitud.status = 'pendiente'
            solicitud.client = client
            solicitud.nombre = form.cleaned_data['nombre']
            solicitud.email = form.cleaned_data['email']
            solicitud.telefono = form.cleaned_data['telefono']
            solicitud.placa = form.cleaned_data['placa']
            solicitud.marca = form.cleaned_data['marca']
            solicitud.submarca = form.cleaned_data['submarca']
            solicitud.modelo = form.cleaned_data['modelo']
            solicitud.ultimo_holograma = form.cleaned_data['holograma']
            solicitud.coche_registrado = False
            solicitud.cupon = cupon
            solicitud.save()
            
            direccion = models.Direccion()
            direccion.solicitud = solicitud
            direccion.calle = form.cleaned_data['calle']
            direccion.numero_exterior = form.cleaned_data['exterior']
            direccion.numero_interior = form.cleaned_data['interior']
            direccion.colonia = form.cleaned_data['colonia']
            direccion.municipio = form.cleaned_data['delegacion']
            direccion.estado = form.cleaned_data['estado']
            direccion.codigo_postal = form.cleaned_data['codigo']
            if 'referencias' in form.data and form.data['referencias'] != '':
                direccion.referencias = form.cleaned_data['referencias']
            direccion.tipo = 'ambos'
            direccion.save()
            
            utilities.send_confirmation_email(solicitud, request)
            token = urlsafe_base64_encode('?folio='+`solicitud.internal_folio()`+'&timestamp='+`utilities.unix_time(timezone.make_naive(solicitud.timestamp_abierto, timezone.utc))`)
            # redirect to a new URL:
            return HttpResponseRedirect(reverse(target, args=(token,)))
        elif 'cupon' in form.data and form.data['cupon'] != '' and form.data['cupon'] != None:
            try:
                cupon = models.Cupon.objects.get(codigo=form.data['cupon'].upper())
            except:
                form.add_error('cupon',u'Cupón inválido')
    else:
        year = timezone.now().year
        if 'cupon' in request.GET:
            form = forms.PublicCreateSolicitudForm(initial={'modelo': `year`, 'holograma':'CERO', 'cupon':request.GET.get('cupon')})
        else: 
            form = forms.PublicCreateSolicitudForm(initial={'modelo': `year`, 'holograma':'CERO'})
    context['form'] = form
    return render(request, template, context)

def create_solicitud_verifica(request):
    return create_solicitud(request, template='drivemee/verifica_create_form.html', source='verifica')