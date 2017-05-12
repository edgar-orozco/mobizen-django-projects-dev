import csv
from servicios.models import *
from decimal import Decimal

def parse():
    with open('servicios.csv', 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                establecimiento = Establecimiento.objects.get(identificador=row['VERIFICENTRO'].strip())
                created = False
            except:
                establecimiento = Establecimiento()
                establecimiento.identificador = row['VERIFICENTRO'].strip()
                created = True
            if created:
                direccion = Direccion()
            else:
                direccion = Direccion.objects.get(establecimiento=establecimiento)

            establecimiento.servicio = Servicio.objects.get(name='verificentros')
            establecimiento.razon_social = row['RAZON'].strip()
            establecimiento.save()
            telefonos = []
            if 'TEL1' in row:
                t1, t1_created = Telefono.objects.get_or_create(telnumber=row['TEL1'].replace(' ',''))
                t1.save()
                telefonos.append(t1)
            if 'TEL2' in row:
                t2, t2_created = Telefono.objects.get_or_create(telnumber=row['TEL2'].replace(' ',''))
                t2.save()
                telefonos.append(t2)
            establecimiento.telefonos = telefonos
            if 'TRAMITE' in row:
                tr = row['TRAMITE'].replace('"','').split(',')
                tramites = []
                for val in tr:
                    tramite, t_created = Tramite.objects.get_or_create(name=val.strip())
                    tramites.append(tramite)
                establecimiento.tramites = tramites
            establecimiento.save()

            estado = row['ESTADO'].strip()
            municipio, m_created = Municipio.objects.get_or_create(name=row['MUNICIPIO'].strip(), estado=estado)
            colonia, c_created = Colonia.objects.get_or_create(name=row['COLONIA'].strip(), municipio=municipio)
#             municipio.save()
#             colonia.save()
            
            direccion.calle = row['CALLE'].strip()
            direccion.estado = estado
            direccion.municipio = municipio
            direccion.colonia = colonia
            try:
                direccion.latitud = Decimal(row['LATITUD'])
            except:
                direccion.latitud = Decimal('0.0')
            try:
                direccion.longitud = Decimal(row['LONGITUD'])
            except:
                direccion.longitud = Decimal('0.0')
            direccion.establecimiento = establecimiento
            direccion.save()

def parse_corralones():
    with open('corralones.csv', 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                establecimiento = Establecimiento.objects.get(identificador=row['CORRALON'].strip())
                created = False
            except:
                establecimiento = Establecimiento()
                establecimiento.identificador = row['CORRALON'].strip()
                created = True
            if created:
                direccion = Direccion()
            else:
                direccion = Direccion.objects.get(establecimiento=establecimiento)

            establecimiento.servicio = Servicio.objects.get(name='corralones')
            establecimiento.razon_social = row['RAZON'].strip()
            establecimiento.save()
            telefonos = []
            if 'TEL1' in row:
                t1, t1_created = Telefono.objects.get_or_create(telnumber=row['TEL1'].replace(' ',''))
                t1.save()
                telefonos.append(t1)
            if 'TEL2' in row:
                t2, t2_created = Telefono.objects.get_or_create(telnumber=row['TEL2'].replace(' ',''))
                t2.save()
                telefonos.append(t2)
            establecimiento.telefonos = telefonos
            establecimiento.save()

            estado = row['ESTADO'].strip()
            municipio, m_created = Municipio.objects.get_or_create(name=row['MUNICIPIO'].strip(), estado=estado)
            colonia, c_created = Colonia.objects.get_or_create(name=row['COLONIA'].strip(), municipio=municipio)
                        
            direccion.calle = row['CALLE'].strip()
            direccion.estado = estado
            direccion.municipio = municipio
            direccion.colonia = colonia
            try:
                direccion.latitud = Decimal(row['LATITUD'])
            except:
                direccion.latitud = Decimal('0.0')
            try:
                direccion.longitud = Decimal(row['LONGITUD'])
            except:
                direccion.longitud = Decimal('0.0')
            direccion.establecimiento = establecimiento
            direccion.save()
