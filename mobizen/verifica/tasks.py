# -*- coding: utf-8 -*- 
from mobizen import celery_app
from verifica import push
from verifica import models
import datetime
import string
import unicodedata
import calendar
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Q
from multiprocessing import Pool

def dia_feriado(fecha=None):
    try:
        feriado = models.Feriado.objects.get(date=fecha)
    except:
        return False
    return True

def weeks_with_saturday(date):
    weeks = calendar.Calendar().monthdayscalendar(date.year, date.month)
    saturday_weeks = []
    for x in range(len(weeks)):
        if bool(weeks[x][5]):
            saturday_weeks += [weeks[x]]
    return saturday_weeks

def week_of_month(date):
    weeks = weeks_with_saturday(date)
    for x in range(len(weeks)):
        if date.day in weeks[x]:
            return x+1

def get_notification_time(date):
    if date.minute >= 0 and date.minute < 10:
        notification_time = str(date.hour)+',10'
    elif date.minute >= 10 and date.minute < 20:
        notification_time = str(date.hour)+',20'
    elif date.minute >= 20 and date.minute < 30:
        notification_time = str(date.hour)+',30'
    elif date.minute >= 30 and date.minute < 40:
        notification_time = str(date.hour)+',40'
    elif date.minute >= 40 and date.minute < 50:
        notification_time = str(date.hour)+',50'
    elif date.minute >= 50 and date.minute < 60:
        notification_time = str(date.hour+1)+',00'
    return notification_time

@celery_app.task()
def mass_push(alert=None):
    if alert:
        push.send_mass_push(alert)
    else:
        push.send_mass_push('prueba')
          
# @celery_app.task(ignore_result=True)
@celery_app.task(rate_limit='6/s', ignore_result=True)
def async_push(deviceToken, alert, sound=None, action=None, badge=None, push_time=None, expiration_time=None, vehiculo=None, other=None, token=None):
    push.send_push(deviceToken=deviceToken, alert=alert, sound=sound, badge=badge, push_time=push_time, action=action, vehiculo=vehiculo, other=other, token=token)

@celery_app.task()
def pulse_notify_mnc_parejo(time_limit=9999):
    """Avisa a los autos que no circulan mañana
       Esta opcion ignora configuracion de HNC/MNC y avisa a todos
       Tambien se ignora el holograma, solo cuando marcaron "Exento HNC" o cuando tiene holograma exento
    """
    now = timezone.localtime(timezone.now())
    day_of_week = now.weekday()
    notification_time = get_notification_time(now)
    if now.weekday() == 6:
        day_of_week = 0
    else:
        day_of_week = now.weekday() + 1
    dia_descanso = day_of_week
    vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & Q(exento=False) & Q(dia_no_circula=dia_descanso) & Q(client__config__hora_alertas_mnc=notification_time) & (Q(verificacion__resultado='CERO') | Q(verificacion__resultado='DOBLE CERO')))
    config_alertas = notification_time.split(',')
    hora = int(config_alertas[0])
    min = int(config_alertas[1])
    for vehiculo in vehiculos:
    #         config = models.AppConfig.objects.get(client=vehiculo.client)
        emoji = unicode('🎉 ', 'utf-8')
        message = u'Termina Hoy No Circula parejo, mañana SI puede circular el auto '+vehiculo.alias
        now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
        naive_date = timezone.make_naive(now, timezone.utc)
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+message, push_time=naive_date.isoformat(), action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(vehiculos)

@celery_app.task()
def pulse_notify_hnc_parejo(time_limit=9999):
    """Avisa a los autos que no circulan hoy
       Esta opcion ignora configuracion de HNC/MNC y avisa a todos
       Tambien se ignora el holograma, solo cuando marcaron "Exento HNC" o cuando tiene holograma exento
    """
    now = timezone.localtime(timezone.now())
    day_of_week = now.weekday()
    notification_time = get_notification_time(now)
    dia_descanso = day_of_week
    vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & Q(exento=False) & Q(dia_no_circula=dia_descanso) & Q(client__config__hora_alertas_hnc=notification_time) & (Q(verificacion__resultado='CERO') | Q(verificacion__resultado='DOBLE CERO')))
    config_alertas = notification_time.split(',')
    hora = int(config_alertas[0])
    min = int(config_alertas[1])
    for vehiculo in vehiculos:
        emoji = unicode('🎉 ', 'utf-8')
        message = u'Termina Hoy No Circula parejo, hoy SI puede circular el auto '+vehiculo.alias
        now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
        naive_date = timezone.make_naive(now, timezone.utc)
        expiration_date = timezone.make_naive(timezone.localtime(timezone.now()).replace(hour=22, minute=0, second=0, microsecond=0), timezone.utc)
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+message, push_time=naive_date.isoformat()+'Z', expiration_time=expiration_date.isoformat()+'Z', action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(vehiculos)

@celery_app.task()
def pulse_notify_mnc_contingencia(time_limit=9999):
    """Avisa a los autos que no circulan mañana
       Esta opcion ignora configuracion de HNC/MNC y avisa a todos
       Tambien se ignora el holograma, solo cuando marcaron "Exento HNC" o cuando tiene holograma exento
    """
    now = timezone.localtime(timezone.now())
    tomorrow = (now+relativedelta(days=+1)).date()
    day_of_week = now.weekday()
    notification_time = get_notification_time(now)
    if now.weekday() == 6:
        day_of_week = 0
    else:
        day_of_week = now.weekday() + 1
    dia_descanso = day_of_week
    if day_of_week == 5:
        week_number = week_of_month(now)
        dia_descanso = 0
        if week_number == 1:
            # Terminacion 5 y 6
            dia_descanso = 0
        elif week_number == 2:
            # Terminacion 7 y 8
            dia_descanso = 1
        elif week_number == 3:
            # Terminacion 3 y 4
            dia_descanso = 2
        elif week_number == 4:
            # Terminacion 1 y 2
            dia_descanso = 3
        else:
            # Semana 5
            # Terminacion 9 y 0
            dia_descanso = 4
    vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & ~Q(verificacion__resultado='EXENTO') & Q(exento=False) & Q(dia_no_circula=dia_descanso) & Q(client__config__hora_alertas_mnc=notification_time))
    config_alertas = notification_time.split(',')
    hora = int(config_alertas[0])
    min = int(config_alertas[1])
    for vehiculo in vehiculos:
    #         config = models.AppConfig.objects.get(client=vehiculo.client)
        if dia_feriado(now+relativedelta(days=+1)) == True:
            emoji = unicode('🎉 ', 'utf-8')
            message = u'Mañana se suspende el Hoy No Circula. El auto '+vehiculo.alias+u' podrá circular'
        else:
            emoji = unicode('🚌 ', 'utf-8')
            message = u'Mañana No Circula el auto '+vehiculo.alias
        now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
        naive_date = timezone.make_naive(now, timezone.utc)
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+message, push_time=naive_date.isoformat(), action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    try:
        contingencia = models.Contingencia.objects.get(vigencia=tomorrow)
    except:
        contingencia = None
    if contingencia:
        terminaciones = []
        for term in contingencia.reglas.all()[0].terminaciones.all():
            terminaciones += term.value
        vehiculos_contigencia = models.Vehiculo.objects.filter(~Q(client='admin') & ~Q(verificacion__resultado='EXENTO') & Q(exento=False) & Q(ultimo_digito__in=terminaciones) & Q(client__config__hora_alertas_mnc=notification_time))
        for vehiculo in vehiculos_contigencia:
            message = u'Contingencia: Mañana No Circula el auto '+vehiculo.alias
            now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
            naive_date = timezone.make_naive(now, timezone.utc)
            async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=message, push_time=naive_date.isoformat()+'Z', action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(vehiculos)

@celery_app.task()
def pulse_notify_mnc(time_limit=9999):
    """Avisa a los autos que no circulan mañana"""
    now = timezone.localtime(timezone.now())
    tomorrow = (now+relativedelta(days=+1)).date()
    day_of_week = now.weekday()
    notification_time = get_notification_time(now)

    if now.weekday() == 6:
        day_of_week = 0
    else:
        day_of_week = now.weekday() + 1
    # Los queries solo toman los autos cuya configuracion tiene activada la alerta de MNC
    if day_of_week == 5:
        week_number = week_of_month(now)
        if week_number == 1 or week_number == 3:
            # Impares
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(Q(Q(es_par=False) & Q(exento=False) & Q(verificacion__resultado='UNO')) | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_mnc = True) & Q(client__config__hora_alertas_mnc=notification_time)))
        elif week_number == 2 or week_number == 4:
            # Pares
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(Q(Q(es_par=True) & Q(exento=False) & Q(verificacion__resultado='UNO')) | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_mnc = True) & Q(client__config__hora_alertas_mnc=notification_time)))
        else:
            # Semana 5 solo los DOS
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(exento=False) & Q(verificacion__resultado='DOS') & Q(client__config__alertas_mnc = True) & Q(client__config__hora_alertas_mnc=notification_time)))
    else:
        vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(dia_no_circula=day_of_week) & Q(exento=False) & Q(Q(verificacion__resultado='UNO') | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_mnc = True) & Q(client__config__hora_alertas_mnc=notification_time)))
    for vehiculo in vehiculos:
#         config = models.AppConfig.objects.get(client=vehiculo.client)
        config_alertas = notification_time.split(',')
        hora = int(config_alertas[0])
        min = int(config_alertas[1])
        if dia_feriado(now+relativedelta(days=+1)) == True:
            emoji = unicode('🎉 ', 'utf-8')
            message = u'Mañana se suspende el Hoy No Circula. El auto '+vehiculo.alias+u' podrá circular'
        else:
            emoji = unicode('🚌 ', 'utf-8')
            message = u'Mañana No Circula el auto '+vehiculo.alias
        now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
        naive_date = timezone.make_naive(now, timezone.utc)
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+message, push_time=naive_date.isoformat()+'Z', action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    try:
        contingencia = models.Contingencia.objects.get(vigencia=tomorrow)
    except:
        contingencia = None
    if contingencia:
        terminaciones = []
        for term in contingencia.reglas.all()[0].terminaciones.all():
            terminaciones += term.value
        hologramas = ['EXENTO','DOBLE CERO', 'CERO']
        vehiculos_contigencia = models.Vehiculo.objects.filter(~Q(client='admin') & ~Q(verificacion__resultado__in=hologramas) & Q(exento=False) & Q(ultimo_digito__in=terminaciones) & Q(client__config__hora_alertas_mnc=notification_time))
        for vehiculo in vehiculos_contigencia:
            message = u'Contingencia: Mañana No Circula el auto '+vehiculo.alias
            now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
            naive_date = timezone.make_naive(now, timezone.utc)
            async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=message, push_time=naive_date.isoformat()+'Z', action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(vehiculos)
  
# @celery_app.task(ignore_result=True)
@celery_app.task()
def pulse_notify_hnc_contingencia(time_limit=9999):
    """Avisa a los autos que no circulan hoy
       Esta opcion ignora configuracion de HNC/MNC y avisa a todos
       Tambien se ignora el holograma, solo cuando marcaron "Exento HNC" o cuando tiene holograma exento
    """
    now = timezone.localtime(timezone.now())
    today = now.date()
    day_of_week = now.weekday()
    notification_time = get_notification_time(now)
    dia_descanso = day_of_week
    if day_of_week == 5:
        week_number = week_of_month(now)
        if week_number == 1:
            # Terminacion 5 y 6
            dia_descanso = 0
        elif week_number == 2:
            # Terminacion 7 y 8
            dia_descanso = 1
        elif week_number == 3:
            # Terminacion 3 y 4
            dia_descanso = 2
        elif week_number == 4:
            # Terminacion 1 y 2
            dia_descanso = 3
        else:
            # Semana 5
            # Terminacion 9 y 0
            dia_descanso = 4
    vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & ~Q(verificacion__resultado='EXENTO') & Q(exento=False) & Q(dia_no_circula=dia_descanso) & Q(client__config__hora_alertas_hnc=notification_time))
    config_alertas = notification_time.split(',')
    hora = int(config_alertas[0])
    min = int(config_alertas[1])
    for vehiculo in vehiculos:
        if dia_feriado(now) == True:
            emoji = unicode('🎉 ', 'utf-8')
            message = u'Hoy se suspende el Hoy No Circula. El auto '+vehiculo.alias+u' puede circular'
        else:
            emoji = unicode('🚫 ', 'utf-8')
            message = u'Hoy No Circula el auto '+vehiculo.alias
        now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
        naive_date = timezone.make_naive(now, timezone.utc)
        expiration_date = timezone.make_naive(timezone.localtime(timezone.now()).replace(hour=22, minute=0, second=0, microsecond=0), timezone.utc)
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+message, push_time=naive_date.isoformat()+'Z', expiration_time=expiration_date.isoformat()+'Z', action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    try:
        contingencia = models.Contingencia.objects.get(vigencia=today)
    except:
        contingencia = None
    if contingencia:
        terminaciones = []
        for term in contingencia.reglas.all()[0].terminaciones.all():
            terminaciones += term.value
        vehiculos_contigencia = models.Vehiculo.objects.filter(~Q(client='admin') & ~Q(verificacion__resultado='EXENTO') & Q(exento=False) & Q(ultimo_digito__in=terminaciones) & Q(client__config__hora_alertas_hnc=notification_time))
        for vehiculo in vehiculos_contigencia:
            message = u'Contingencia: Hoy No Circula el auto '+vehiculo.alias
            now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
            naive_date = timezone.make_naive(now, timezone.utc)
            async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=message, push_time=naive_date.isoformat()+'Z', action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(vehiculos)

@celery_app.task()
def pulse_notify_hnc(time_limit=9999):
    """Avisa a los autos que no circulan hoy"""
    now = timezone.localtime(timezone.now())
    today = now.date()
    day_of_week = now.weekday()
    notification_time = get_notification_time(now)
    
    # Los queries solo toman los autos cuya configuracion tiene activada la alerta de HNC
    if day_of_week == 5:
        week_number = week_of_month(now)
        if week_number == 1 or week_number == 3:
            # Impares
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(Q(Q(es_par=False) & Q(exento=False) & Q(verificacion__resultado='UNO')) | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_hnc = True) & Q(client__config__hora_alertas_hnc=notification_time)))
        elif week_number == 2 or week_number == 4:
            # Pares
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(Q(Q(es_par=True) & Q(exento=False) & Q(verificacion__resultado='UNO')) | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_hnc = True) & Q(client__config__hora_alertas_hnc=notification_time)))
        else:
            # Semana 5 solo los DOS
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(exento=False) & Q(verificacion__resultado='DOS') & Q(client__config__alertas_hnc = True) & Q(client__config__hora_alertas_hnc=notification_time)))
    else:
        vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(dia_no_circula=day_of_week) & Q(exento=False) & Q(Q(verificacion__resultado='UNO') | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_hnc = True) & Q(client__config__hora_alertas_hnc=notification_time)))
    for vehiculo in vehiculos:
    #         config = models.AppConfig.objects.get(client=vehiculo.client)
        config_alertas = notification_time.split(',')
        hora = int(config_alertas[0])
        min = int(config_alertas[1])
        if dia_feriado(now) == True:
            emoji = unicode('🎉 ', 'utf-8')
            message = u'Hoy se suspende el Hoy No Circula. El auto '+vehiculo.alias+u' puede circular'
        else:
            emoji = unicode('🚫 ', 'utf-8')
            message = u'Hoy No Circula el auto '+vehiculo.alias
        now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
        naive_date = timezone.make_naive(now, timezone.utc)
        expiration_date = timezone.make_naive(timezone.localtime(timezone.now()).replace(hour=22, minute=0, second=0, microsecond=0), timezone.utc)
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+message, push_time=naive_date.isoformat()+'Z', expiration_time=expiration_date.isoformat()+'Z', action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    try:
        contingencia = models.Contingencia.objects.get(vigencia=today)
    except:
        contingencia = None
    if contingencia:
        terminaciones = []
        for term in contingencia.reglas.all()[0].terminaciones.all():
            terminaciones += term.value
        hologramas = ['EXENTO','DOBLE CERO', 'CERO']
        vehiculos_contigencia = models.Vehiculo.objects.filter(~Q(client='admin') & ~Q(verificacion__resultado__in=hologramas) & Q(exento=False) & Q(ultimo_digito__in=terminaciones) & Q(client__config__hora_alertas_hnc=notification_time))
        for vehiculo in vehiculos_contigencia:
            message = u'Contingencia: Hoy No Circula el auto '+vehiculo.alias
            now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
            naive_date = timezone.make_naive(now, timezone.utc)
            async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=message, push_time=naive_date.isoformat()+'Z', action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
        return len(vehiculos)

@celery_app.task()
def notify_hnc(time_limit=9999):
    """Avisa a los autos que no circulan hoy"""
    now = timezone.localtime(timezone.now())
    day_of_week = now.weekday()
    # Los queries solo toman los autos cuya configuracion tiene activada la alerta de HNC
    if day_of_week == 5:
        week_number = week_of_month(now)
        if week_number == 1 or week_number == 3:
            # Impares
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(Q(Q(es_par=False) & Q(exento=False) & Q(verificacion__resultado='UNO')) | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_hnc = True)))
        elif week_number == 2 or week_number == 4:
            # Pares
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(Q(Q(es_par=True) & Q(exento=False) & Q(verificacion__resultado='UNO')) | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_hnc = True)))
        else:
            # Semana 5 solo los DOS
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(exento=False) & Q(verificacion__resultado='DOS') & Q(client__config__alertas_hnc = True)))
    else:
        vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(dia_no_circula=day_of_week) & Q(exento=False) & Q(Q(verificacion__resultado='UNO') | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_hnc = True)))
    for vehiculo in vehiculos:
        config = models.AppConfig.objects.get(client=vehiculo.client)
        config_alertas = config.hora_alertas_hnc.split(',')
        hora = int(config_alertas[0])
        min = int(config_alertas[1])
        now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
        naive_date = timezone.make_naive(now, timezone.utc)
        expiration_date = timezone.make_naive(timezone.localtime(timezone.now()).replace(hour=22, minute=0, second=0, microsecond=0), timezone.utc)
        emoji = unicode('🎉 ', 'utf-8')
        alert = u'Mañana no circula el auto '+vehiculo.alias
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+alert, push_time=naive_date.isoformat()+'Z', expiration_time=expiration_date.isoformat()+'Z', action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(vehiculos)

@celery_app.task()
def notify_mnc(time_limit=9999):
    """Avisa a los autos que no circulan mañana"""
    now = timezone.localtime(timezone.now())
    if now.weekday() == 6:
        day_of_week = 0
    else:
        day_of_week = now.weekday() + 1
    # Los queries solo toman los autos cuya configuracion tiene activada la alerta de MNC
    if day_of_week == 5:
        week_number = week_of_month(now)
        if week_number == 1 or week_number == 3:
            # Impares
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(Q(Q(es_par=False) & Q(exento=False) & Q(verificacion__resultado='UNO')) | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_mnc = True)))
        elif week_number == 2 or week_number == 4:
            # Pares
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(Q(Q(es_par=True) & Q(exento=False) & Q(verificacion__resultado='UNO')) | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_mnc = True)))
        else:
            # Semana 5 solo los DOS
            vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(exento=False) & Q(verificacion__resultado='DOS') & Q(client__config__alertas_mnc = True)))
    else:
        vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & (Q(dia_no_circula=day_of_week) & Q(exento=False) & Q(Q(verificacion__resultado='UNO') | Q(verificacion__resultado='DOS')) & Q(client__config__alertas_mnc = True)))
    for vehiculo in vehiculos:
        config = models.AppConfig.objects.get(client=vehiculo.client)
        config_alertas = config.hora_alertas_mnc.split(',')
        hora = int(config_alertas[0])
        min = int(config_alertas[1])
        now = now.replace(hour=hora, minute=min, second=0, microsecond=0)
        naive_date = timezone.make_naive(now, timezone.utc)
        emoji = unicode('🚌 ', 'utf-8')
        alert = u'Hoy No Circula el auto '+vehiculo.alias
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+alert, push_time=naive_date.isoformat()+'Z', action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(vehiculos)


@celery_app.task()
def notify_fin_tarjeta_circulacion(time_limit=9999):
    now = timezone.localtime(timezone.now())
    vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & Q(tarjeta_circulacion_vigencia = now) & Q(tarjeta_circulacion_permanente=False))
    for vehiculo in vehiculos:
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=u'La tarjeta de circulación del auto '+vehiculo.alias+u' vence hoy', badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(vehiculos)

@celery_app.task()
def notify_quincena_seguro(time_limit=9999):
    now = timezone.localtime(timezone.now())
    seguros = models.Seguro.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now + datetime.timedelta(days=14)))
    for seguro in seguros:
        vehiculo = seguro.vehiculo
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=u'El seguro del auto '+vehiculo.alias+u' vence en dos semanas. Renuévalo desde Verifica', badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(seguros)

@celery_app.task()
def notify_semana_seguro(time_limit=9999):
    now = timezone.localtime(timezone.now())
    seguros = models.Seguro.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now + datetime.timedelta(days=7)))
    for seguro in seguros:
        vehiculo = seguro.vehiculo
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=u'El seguro del auto '+vehiculo.alias+u' vence en una semana. Renuévalo desde Verifica', badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(seguros)

@celery_app.task()
def notify_fin_seguro(time_limit=9999):
    now = timezone.localtime(timezone.now())
    seguros = models.Seguro.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now))
    for seguro in seguros:
        vehiculo = seguro.vehiculo
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=u'El seguro del auto '+vehiculo.alias+u' vence hoy. Renuévalo desde Verifica', badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(seguros)

@celery_app.task()
def notify_mes_seguro_vencido(time_limit=9999):
    now = timezone.localtime(timezone.now())
    seguros = models.Seguro.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now + relativedelta(months=-1)))
    for seguro in seguros:
        vehiculo = seguro.vehiculo
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=u'Recuerda que el seguro del auto '+vehiculo.alias+u' venció. No corras riesgos, asegúrate ahora mismo', badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(seguros)

@celery_app.task()
def notify_2mes_seguro_vencido(time_limit=9999):
    now = timezone.localtime(timezone.now())
    seguros = models.Seguro.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now + relativedelta(months=-2)))
    for seguro in seguros:
        vehiculo = seguro.vehiculo
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=u'Recuerda que el seguro del auto '+vehiculo.alias+u' venció. No corras riesgos, asegúrate ahora mismo', badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(seguros)

@celery_app.task()
def notify_3mes_seguro_vencido(time_limit=9999):
    now = timezone.localtime(timezone.now())
    seguros = models.Seguro.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now + relativedelta(months=-3)))
    for seguro in seguros:
        vehiculo = seguro.vehiculo
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=u'Recuerda que el seguro del auto '+vehiculo.alias+u' venció. No corras riesgos, asegúrate ahora mismo', badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(seguros)

@celery_app.task()
def notify_semana_seguro_vencido(time_limit=9999):
    now = timezone.localtime(timezone.now())
    seguros = models.Seguro.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now + relativedelta(days=-7)))
    for seguro in seguros:
        vehiculo = seguro.vehiculo
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=u'El seguro del auto '+vehiculo.alias+u' se encuentra vencido. Asegúrate ahora y no te quedes desprotegido', badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(seguros)

@celery_app.task()
def notify_inicio_verificacion(time_limit=9999):
    now = timezone.localtime(timezone.now())
    verificaciones = models.Verificacion.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now+relativedelta(months=+1, day=31)) & Q(vehiculo__config__alerta_inicio = True))
    for verificacion in verificaciones:
        vehiculo = verificacion.vehiculo
        emoji = unicode('🚨 ', 'utf-8')
        alert = u'Verificación: Inicia Periodo para el auto '+vehiculo.alias+u'. ¡Solicita el Servicio a Domicilio y no pierdas tiempo!'
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+alert, badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(verificaciones)

@celery_app.task()
def notify_mitad_verificacion(time_limit=9999):
    now = timezone.localtime(timezone.now())
    verificaciones = models.Verificacion.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now+relativedelta(day=31)) & Q(vehiculo__config__alerta_mes = True))
    for verificacion in verificaciones:
        vehiculo = verificacion.vehiculo
        emoji = unicode('🚨 ', 'utf-8')
        alert = u'Verificación: Resta un mes para verificar el auto '+vehiculo.alias+u'. ¡Solicita el Servicio a Domicilio y no pierdas tiempo!'
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+alert, badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(verificaciones)

@celery_app.task()
def notify_quincena_verificacion(time_limit=9999):
    now = timezone.localtime(timezone.now())
    verificaciones = models.Verificacion.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now + datetime.timedelta(days=14)) & Q(vehiculo__config__alerta_quincena = True))
    for verificacion in verificaciones:
        vehiculo = verificacion.vehiculo
        emoji = unicode('🚨 ', 'utf-8')
        alert = u'Verificación: Restan dos semanas para verificar el auto '+vehiculo.alias+u'. ¡Solicita el Servicio a Domicilio y no pierdas tiempo!'
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+alert, badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(verificaciones)

@celery_app.task()
def notify_semana_verificacion(time_limit=9999):
    now = timezone.localtime(timezone.now())
    verificaciones = models.Verificacion.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now + datetime.timedelta(days=7)) & Q(vehiculo__config__alerta_semana = True))
    for verificacion in verificaciones:
        vehiculo = verificacion.vehiculo
        emoji = unicode('🚨 ', 'utf-8')
        alert = u'Verificación: Resta una semana para verificar el auto '+vehiculo.alias+u'. ¡Solicita el Servicio a Domicilio y no pierdas tiempo!'
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+alert, badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(verificaciones)

@celery_app.task()
def notify_fin_verificacion(time_limit=9999):
    now = timezone.localtime(timezone.now())
    verificaciones = models.Verificacion.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now) & Q(vehiculo__config__alerta_fin = True))
    for verificacion in verificaciones:
        vehiculo = verificacion.vehiculo
        emoji = unicode('🚨 ', 'utf-8')
        alert = u'Verificación: Hoy termina el periodo de verificación para el auto '+vehiculo.alias+u'.'
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+alert, badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(verificaciones)

def notify_verificacion_monday(time_limit=9999):
    now = timezone.localtime(timezone.now())
    start = now.replace(day=1).date()
    end = now + relativedelta(months=+1, day=31)
    verificaciones = models.Verificacion.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia__gt = start) & Q(vigencia__lte=end))
    for verificacion in verificaciones:
        vehiculo = verificacion.vehiculo
        emoji = unicode('🚨 ', 'utf-8')
        alert = u'Verificación: El auto '+vehiculo.alias+u' se encuentra en periodo de verificación. ¡Solicita nuestro Servicio a Domicilio y no pierdas tiempo!'
        async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=emoji+alert, badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
    return len(verificaciones)

# @celery_app.task()
# def notify_no_asegurados():
#     now = timezone.localtime(timezone.now())
#     vehiculos = models.Vehiculo.objects.filter(seguro=None).distinct()
#     client_list = []
#     for v in vehiculos:
#         client_list += [v.client.deviceToken]
#     clean_set = set(client_list)
#     verificaciones = models.Verificacion.objects.filter(~Q(vehiculo__client='admin') & Q(vigencia = now) & Q(vehiculo__config__alerta_fin = True))
#     for verificacion in verificaciones:
#         vehiculo = verificacion.vehiculo
#         async_push.delay(deviceToken=vehiculo.client.deviceToken, alert=u'El auto '+vehiculo.alias+u' termina periodo de verificación', badge=True, action='verifica.showInfo', vehiculo=vehiculo.id, sound=' ')
#     return len(verificaciones)

@celery_app.task()
def scrape_all_vehiculos():
    vehiculos = models.Vehiculo.objects.filter(~Q(client='admin'))
    total = {'Pass': 0, 'Fail': 0}
    for vehiculo in vehiculos:
        result = vehiculo.fetch_info(send_push=True)
        if result == True:
            total['Pass'] += 1
        else:
            total['Fail'] += 1
    return total

@celery_app.task()
def scrape_partial_vehiculos():
    now = timezone.now()
    last_free_update = now + relativedelta(days=-5, hour=0, minute=0, second=0, microsecond=0)
    last_paid_update = now + relativedelta(days=-1, hour=0, minute=0, second=0, microsecond=0)
    vehiculos = models.Vehiculo.objects.filter(~Q(client='admin') & Q(Q((last_update__gte=last_update) & Q(client__account__account_type='free')) | Q(Q((last_update__gte=last_update) & Q(client__account__account_type='free')))))
    total = {'Pass': 0, 'Fail': 0}
    for vehiculo in vehiculos:
        result = vehiculo.fetch_info(send_push=True)
        if result == True:
            total['Pass'] += 1
        else:
            total['Fail'] += 1
    return total

@celery_app.task(rate_limit='120/m', default_retry_delay=2 * 60, max_retries=1, time_limit=15)
def fetch_vehiculo(vehiculo_id):
    vehiculo = models.Vehiculo.objects.get(id=vehiculo_id)
    result = vehiculo.fetch_info(send_push=True)
    try:
        if result is not True:
            raise Exception
    except:
        raise fetch_vehiculo.retry(vehiculo_id)
    return result

@celery_app.task(time_limit=9999)
def async_scrape():
    vehiculos = models.Vehiculo.objects.filter(~Q(client='admin'))
    total = {'Pass': 0, 'Fail': 0}
    for vehiculo in vehiculos:
        result = fetch_vehiculo.delay(vehiculo_id=vehiculo.id)
        if result == True:
            total['Pass'] += 1
        else:
            total['Fail'] += 1
    return total    
    
