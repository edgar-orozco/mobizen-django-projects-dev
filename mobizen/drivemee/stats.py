from django.utils import timezone
from django.core.mail import EmailMessage
import datetime
import io

from drivemee import models
from verifica import placa_detector

def make_solicitudes_dump():
    solicitudes = models.Solicitud.objects.all().order_by('pk')
    csv = u'"folio","timestamp_abierto","timestamp_cerrado","timestamp_agendado","timestamp_proceso","nombre","email","telefono","placa","marca","submarca","modelo","ultimo_holograma","coche_registrado","status",""client_id","cupon_id","operador_id","solicitudToken_id","vehiculo_id","costo_real","linked_solicitudes_id","snooze_until_date","sent_reminder_email","timestamp_confirmacion","operador","entidad","coordinador","resultado","tarjeta"\n'
    for sol in solicitudes:
        try:
            folio = str(sol.folio)
            ts_abierto = timezone.make_naive(sol.timestamp_abierto)
            timestamp_abierto = ts_abierto.strftime('%Y-%m-%d %H:%M:%S')
            try:
                ts_cerrado = timezone.make_naive(sol.timestamp_cerrado)
                timestamp_cerrado = ts_cerrado.strftime('%Y-%m-%d %H:%M:%S')
            except:
                timestamp_cerrado = str(None)
            try:
                ts_agendado = timezone.make_naive(sol.timestamp_agendado)
                timestamp_agendado = ts_agendado.strftime('%Y-%m-%d %H:%M:%S')
            except:
                timestamp_agendado = str(None)
            try:
                ts_proceso = timezone.make_naive(sol.timestamp_proceso)
                timestamp_proceso = ts_proceso.strftime('%Y-%m-%d %H:%M:%S')
            except:
                timestamp_proceso = str(None)
            try:
                ts_confirmacion = timezone.make_naive(sol.timestamp_confirmacion)
                timestamp_confirmacion = ts_confirmacion.strftime('%Y-%m-%d %H:%M:%S')
            except:
                timestamp_confirmacion = str(None)
            try:
                ts_snoozed = timezone.make_naive(sol.timestamp_snoozed)
                timestamp_snoozed = ts_snoozed.strftime('%Y-%m-%d %H:%M:%S')
            except:
                timestamp_snoozed = str(None)
            try:
                entidad = placa_detector.parse_placa(sol.placa).estado
            except:
                entidad = ''
            if not entidad:
                entidad = 'Otro'
            if entidad is 'DIF':
                entidad = 'CDMX'
            try:
                cupon = str(sol.cupon.pk)
            except:
                cupon = str(None)
            try:
                operador_id = str(sol.operador.pk)
                operador_name = sol.operador.nombre
            except:
                operador_id = str(None)
                operador_name = str(None)
            try:
                vehiculo_id = str(sol.vehiculo.pk)
            except:
                vehiculo_id = str(None)
            try:
                costo = str(sol.costo_real)
            except:
                costo = str(None)
            try:
                linked = str(sol.linked_solicitudes_id)
            except:
                linked = str(None)
            try:
                coordinador = sol.proveedor.nombre
            except:
                coordinador = str(None)
            try:
                holograma = sol.ultimo_holograma
            except:
                holograma = str(None)
            modelo = str(sol.modelo)
            reminder = str(False)
            registrado = str(sol.coche_registrado)
            try:
                client = sol.client.pk
            except:
                client = str(None)
            try:
                result = sol.resultado.resultado
            except:
                result = str(None)
            try:
                recibo = sol.recibo
                pagado = recibo.status
            except:
                pagado = str(None)
            line = '"'+folio+'","'+timestamp_abierto+'","'+timestamp_cerrado+'","'+timestamp_agendado+'","'+timestamp_proceso+'","'+sol.nombre+'","'+sol.email+'","'+sol.telefono+'","'+sol.placa+'","'+sol.marca+'","'+sol.submarca+'","'+modelo+'","'+holograma+'","'+registrado+'","'+sol.status+'","'+client+'","'+cupon+'","'+operador_id+'","'+sol.solicitudToken.deviceToken+'","'+vehiculo_id+'","'+costo+'","'+linked+'","'+timestamp_snoozed+'","'+reminder+'","'+timestamp_confirmacion+'","'+operador_name+'","'+entidad+'","'+coordinador+'","'+result+'","'+pagado+'"\n'
            
            csv += line
        except:
            print sol.pk
    return csv

def send_dump():
    date = timezone.now()
    csv = make_solicitudes_dump()
    timestamp = date.strftime('%Y%m%d-%H%M%S')
    filename = u'./solicitudes-'+timestamp+'.csv'
    with io.open(filename,'w',encoding='utf8') as f:
        f.write(csv)
    file = None
    with io.open(filename,'r',encoding='utf8') as f:
        file = f.read()
    subject = 'Reporte '+timestamp
    content = ''
    from_email = 'no-reply@verifica.mx'
    to_list = ['cchacon@mobizen.com.mx','jhuerta@mobizen.com.mx']
    msg = EmailMessage(subject, content, from_email, to_list, cc=None, bcc=None)
    msg.attach_file(filename)
    msg.content_subtype = "text"
    msg.send()
