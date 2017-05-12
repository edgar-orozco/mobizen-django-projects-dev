import requests, json
from verifica.models import Imeca
import datetime
from django.utils import timezone

def parse_imecas():
    req = requests.get('http://148.243.232.113/calidadaire/xml/simat.json')
    try:
        data = req.json()
    except UnicodeDecodeError:
        req.encoding = 'utf-8'
        data = req.json()
    if 'pollutionMeasurements' in data:
        main_node = data['pollutionMeasurements']
        info = main_node['information'][0]
        report_fecha = main_node['timeStamp']
        report_hora = main_node['report']
        indice = info['indiceradiacion'].replace('.PNG','')
        try:
            maxVal = info.get('valormeca')
            maxPollutant = info.get('parametro')
        except:
            maxVal = None
            maxPollutant = None
        if not maxVal:
            maxVal = 0        
            maxPollutant = ''
            for delegation in main_node['delegations']:
                if 'imecaPoints' in delegation:
                    key = 'imecaPoints'
                else:
                    key = 'imATIPoints'
                if delegation[key] is not 'N.D.':
                    try:
                        val = int(delegation[key])
                    except:
                        val = 0
                    if val > maxVal:
                        maxVal = int(delegation[key])
                        maxPollutant = delegation['pollutant']
            for station in main_node['stations']:
                if 'imecaPoints' in station:
                    key = 'imecaPoints'
                else:
                    key = 'imATIPoints'
                if station[key] is not 'N.D.':
                    try:
                        val = int(station[key])
                    except:
                        val = 0
                    if val > maxVal:
                        maxVal = int(station[key])
                        maxPollutant = station['pollutant']
        if not indice:
            indice = '0'
        report, created = Imeca.objects.get_or_create(imecas=str(maxVal), particula=maxPollutant, hora=report_hora, fecha=report_fecha, indice_uv=indice)
    return report;

def most_recent_report():
    now = timezone.localtime(timezone.now())
    last_report = Imeca.objects.filter(hora=`now.hour`,fecha=now.date())
    if last_report:
        return last_report[0]
    new_report = parse_imecas()
    if new_report.fecha < now.date():
        most_recent = Imeca.objects.all()[0]
        return most_recent
    return new_report