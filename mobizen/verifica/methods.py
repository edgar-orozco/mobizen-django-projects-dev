from verifica import models
import requests

def fetch_info(request)
    req = requests.get('http://datos.labplc.mx/movilidad/vehiculos/876TSS.json')
    return req.json()