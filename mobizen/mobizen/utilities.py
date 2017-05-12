# -*- coding: utf-8 -*- 
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time(dt):
    return (dt - epoch).total_seconds()

def date_from_unix_time(milliseconds):
    try:
        milliseconds = float(milliseconds)
    except:
        return None
    return datetime.datetime.utcfromtimestamp(milliseconds)

def send_confirmation_email(solicitud, request=None):
    subject = "Confirmar Solicitud"
    to = [solicitud.email]
    from_email = 'no-reply@verifica.mx'

    if request:
        domain = request.build_absolute_uri('/')[:-1]
    else:
        domain = 'https://app.verifica.mx/'
#         domain = 'http://104.131.133.40/'
    encode_string = urlsafe_base64_encode('?confirmFolio='+str(solicitud.folio))
    ctx = {
        'folio': solicitud.internal_folio(),
        'confirmation_string': encode_string,
        'domain': domain
    }
    message = get_template('drivemee/verifica_solicitud_email.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

def send_lead_email(solicitud, request):
    subject = "Nuevo Lead"
    to = ["callcenter@mobizen.com.mx", "verifica@mobizen.com.mx"]
    from_email = 'no-reply@verifica.mx'
    ctx = {
        'folio': solicitud.internal_folio(),
        'solicitud': solicitud.pk,
        'domain': request.build_absolute_uri('/')[:-1]
    }
    message = get_template('drivemee/nuevo_lead_email.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
