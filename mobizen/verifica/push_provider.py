import csv
import json
from verifica import models

def import_from_parse():
    valid_count = 0
    with open('installations.json', 'rb') as f:
        parse_db = json.load(f)
        users = parse_db.get('results')
        for user in users:
            if user.get('userToken'):
                try:
                    client = models.Client.objects.get(deviceToken=user.get('userToken'))
                except:
                    client = None
                if client:
                    valid_count+=1
                    device,created = models.DeviceInfo.objects.get_or_create(client=client)
                    device.parse_token = user.get('installationId')
                    device.push_token = user.get('deviceToken')
                    device.device_os = user.get('deviceType')
                    device.save()
    return valid_count
    
def match_parse_to_onesignal():
    with open('users.csv', 'rb') as f:
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
