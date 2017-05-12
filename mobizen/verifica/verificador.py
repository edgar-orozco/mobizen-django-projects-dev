# -*- coding: utf-8 -*- 
from verifica import models, placa_detector
import datetime
import calendar
import string
import unicodedata
from dateutil import relativedelta
from django.utils import timezone

def semestre_actual():
    today = datetime.datetime.today()
    return 1 if today.month <= 6 else 2

def meses_puede_verificar(ultimo_digito):
    return [meses_verifica_en_semestre(ultimo_digito, semestre_actual())]

def meses_verifica_en_semestre(ultimo_digito, semestre):
    year = timezone.now().year
    if semestre is 2:
        return {
            1: (datetime.datetime(year,10,1),datetime.datetime(year,11,1)),
            2: (datetime.datetime(year,10,1),datetime.datetime(year,11,1)),
            3: (datetime.datetime(year,9,1),datetime.datetime(year,10,1)),
            4: (datetime.datetime(year,9,1),datetime.datetime(year,10,1)),
            5: (datetime.datetime(year,7,1),datetime.datetime(year,8,1)),
            6: (datetime.datetime(year,7,1),datetime.datetime(year,8,1)),
            7: (datetime.datetime(year,8,1),datetime.datetime(year,9,1)),
            8: (datetime.datetime(year,8,1),datetime.datetime(year,9,1)),
            9: (datetime.datetime(year,11,1),datetime.datetime(year,12,1)),
            0: (datetime.datetime(year,11,1),datetime.datetime(year,12,1)),
        }.get(ultimo_digito, (datetime.datetime(year,11,1),datetime.datetime(year,12,1)))
    else:    
        return {
            1: (datetime.datetime(year,4,1),datetime.datetime(year,5,1)),
            2: (datetime.datetime(year,4,1),datetime.datetime(year,5,1)),
            3: (datetime.datetime(year,3,1),datetime.datetime(year,4,1)),
            4: (datetime.datetime(year,3,1),datetime.datetime(year,4,1)),
            5: (datetime.datetime(year,1,1),datetime.datetime(year,2,1)),
            6: (datetime.datetime(year,1,1),datetime.datetime(year,2,1)),
            7: (datetime.datetime(year,2,1),datetime.datetime(year,3,1)),
            8: (datetime.datetime(year,2,1),datetime.datetime(year,3,1)),
            9: (datetime.datetime(year,5,1),datetime.datetime(year,6,1)),
            0: (datetime.datetime(year,5,1),datetime.datetime(year,6,1)),
        }.get(ultimo_digito, (datetime.datetime(year,5,1),datetime.datetime(year,6,1)))

def ultimo_digito(placa):
    _placa = unicodedata.normalize('NFKD', placa).encode('ascii','ignore')
    digitos = _placa.translate(None, string.letters)
    return int(digitos[-1:])
    
def mes_fin_periodo_verificacion(ultimo_digito, semestre):
    if semestre is 1:
        return {
            1: 11,
            2: 11,
            3: 10,
            4: 10,
            5: 8,
            6: 8,
            7: 9,
            8: 9,
            9: 12,
            0: 12,
        }.get(ultimo_digito, 11)
    else:    
        return {
            1: 5,
            2: 5,
            3: 4,
            4: 4,
            5: 2,
            6: 2,
            7: 3,
            8: 3,
            9: 6,
            0: 6,
        }.get(ultimo_digito, 6)

def is_extemporaneo(ultimo_digito, semestre):
    today = datetime.datetime.today()
    semestre = 1 if semestre == 2 else 2
    mes_fin = mes_fin_periodo_verificacion(ultimo_digito, semestre)
    return True if today.month > mes_fin else False

def is_placa_extemporaneo(placa):
    placa = placa.replace(' ','').replace('-','')
    digito = ultimo_digito(placa)
    today = datetime.datetime.today()
    semestre = semestre_actual()
    semestre -= 1
    mes_fin = mes_fin_periodo_verificacion(digito, semestre)
    return True if today.month > mes_fin else False

def vigencia_verificacion(placa, holograma):
    """
    Calcula la próxima vigencia de verificación
    Por el momento ignora el estado
    """
    placa = placa.replace(' ','').replace('-','')
    digito = ultimo_digito(placa)
    semestre = semestre_actual()
    years = 0
    if holograma == 'DOBLE_CERO':
        # Si es 00 se calcula 2 años despues en el mismo semestre que se verificó
        # Excepto si es: a. Placa del DF y b. 'Extemporaneo' sobre su propio semestre; En estos casos aplica regla 1.7
        extemporaneo = is_extemporaneo(digito, semestre)
        try:
            tipo_placa = placa_detector.parse_placa(placa)
        except:
            tipo_placa = None
        if tipo_placa and tipo_placa.estado == 'DIF' and extemporaneo:
            if semestre == 1:
                years = 2
            else:
                semestre = 1
                years = 3
        else:
            semestre = 1 if semestre == 2 else 2
            years = 2
    else:
        if semestre == 2:
            years = 1
    mes_fin = mes_fin_periodo_verificacion(digito, semestre)
    new_date = datetime.datetime.today()+relativedelta.relativedelta(years=+years, month=mes_fin, day=31, hour=12, minute=0, second=0)
    return new_date

def last_week_of_month(date):
    weeks = calendar.Calendar().monthdayscalendar(date.year, date.month)
    if weeks[len(weeks)-1].count(0) > 3:
        return len(weeks)-1
    return len(weeks)

def week_of_month(date):
    weeks = calendar.Calendar().monthdayscalendar(date.year, date.month)
    for x in range(len(weeks)):
        if date.day in weeks[x]:
            return x+1

def is_ultima_semana_periodo(date):
    if date.month == 1 or date.month == 7:
        return False
    return week_of_month(date)>=last_week_of_month(date)
    
def is_periodo_started(placa, date):
    digito = ultimo_digito(placa)
    meses = meses_puede_verificar(digito)[0]
    for periodo in meses:
        if periodo.month == date.month:
            return True
    return False