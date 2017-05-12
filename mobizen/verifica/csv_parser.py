import csv
from verifica.models import Aseguradora, Telefono


def parse():
    with open('aseguradoras.csv', 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            a = Aseguradora()
            a.name = row['NOMBRE COMERCIAL']
            a.save()
            if not row['DF'] == '':
                t = Telefono()
                t.title = 'DF'
                t.telnumber = row['DF']
                t.aseguradora = a
                t.save()
            if not row['INTERIOR'] == '':
                t = Telefono()
                t.title = 'Interior'
                t.telnumber = row['INTERIOR']
                t.aseguradora = a
                t.save()
