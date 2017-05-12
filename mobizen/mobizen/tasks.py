# -*- coding: utf-8 -*- 
from mobizen import celery_app
from verifica import push
from verifica.tasks import async_push
from drivemee import models, utilities

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Q
import datetime

@celery_app.task(rate_limit='2/s', ignore_result=True)
def async_email(request=None, solicitud=None):
    utilities.send_confirmation_email(solicitud=solicitud, request=request)

@celery_app.task()
def change_solicitud_status(time_limit=9999):
    """Busca las solicitudes que ya pasaron la hora agendada y les avisa que ya esta en proceso"""
    now = timezone.localtime(timezone.now())
    notification_time = 'now'
    solicitudes = models.Solicitud.objects.filter(Q(status='agendado') & Q(cita__fecha__range=(now+relativedelta(minutes=-15),now+relativedelta(minutes=+2))))
    for solicitud in solicitudes:
        solicitud.status = 'proceso'
        solicitud.timestamp_proceso = timezone.now()
        solicitud.save()
        if solicitud.vehiculo:
            vehiculo = solicitud.vehiculo.alias
        else:
            vehiculo = solicitud.placa
        async_push.delay(deviceToken=solicitud.client.deviceToken, alert=u'Servicio de Valet para el auto '+vehiculo+u' en proceso.', push_time='now', action='verifica.showValet', token=solicitud.solicitudToken.deviceToken, sound=' ')
    return len(solicitudes)

@celery_app.task()
def solicitud_reminder(time_limit=9999):
    """Busca las solicitudes que inician dentro de 1h y manda aviso. Si ya se asigno un operador, se comunica el nombre"""
    now = timezone.localtime(timezone.now())
    notification_time = 'now'
    solicitudes = models.Solicitud.objects.filter(Q(status='agendado') & Q(cita__fecha__range=(now+datetime.timedelta(hours=1),now+datetime.timedelta(hours=1, minutes=10))))
    for solicitud in solicitudes:
        if solicitud.vehiculo:
            vehiculo = solicitud.vehiculo.alias
        else:
            vehiculo = solicitud.placa
        msg = u'Recordatorio: Servicio de Verificación a Domicilio para el vehículo '+vehiculo+' dentro de 1 hora.'
        if solicitud.operador:
            msg = msg+' El operador asignado es: '+solicitud.operador.nombre
        solicitud.timestamp_proceso = timezone.now()
        solicitud.save()
        async_push.delay(deviceToken=solicitud.client.deviceToken, alert=msg, push_time='now', action='verifica.showValet', token=solicitud.solicitudToken.deviceToken)
    return len(solicitudes)

@celery_app.task()
def notify_pending_solicitudes(time_limit=9999):
    """
    Busca las solicitudes que se crearon y se quedaron pendientes por más de 48hr 
    Se les manda un mail para que puedan confirmar
    """
    now = timezone.localtime(timezone.now())
    solicitudes = models.Solicitud.objects.filter(Q(status='pendiente') & Q(sent_reminder_email=False) & Q(timestamp_abierto__lte=(now-datetime.timedelta(days=2))))
    for solicitud in solicitudes:
        async_email(solicitud=solicitud)
        solicitud.sent_reminder_email = True
        solicitud.save()
    return len(solicitudes)    

@celery_app.task()
def purge_pending_solicitudes(time_limit=9999):
    """
    Busca las solicitudes que se crearon y se quedaron pendientes por más de 1 semana para poder borrarlas
    """
    now = timezone.localtime(timezone.now())
    solicitudes = models.Solicitud.objects.filter(Q(status='pendiente') & Q(timestamp_abierto__lte=(now-datetime.timedelta(days=7))))
    for solicitud in solicitudes:
        solicitud.status = 'abandonada'
        solicitud.save()
    return len(solicitudes)
