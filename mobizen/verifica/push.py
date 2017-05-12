# -*- coding: utf-8 -*- 
import requests
import json
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta
from verifica.models import AppConfig, Client, DeviceInfo

Parse_Application_Id = 'KfAdCrtEsY0ZllOeJ2CadtdLBh4WxSGk8H9HSYVb'
Parse_REST_Key = '2C3TikwgOR6VbxMQcJNNWSscCowabIE1W7dNotK6'

OneSignal_App_Id = '97a05266-5f4a-405d-b187-7e3dc8762af1'
OneSignal_REST_Key = 'MDY0ZTYwZmYtOWJlNy00ZTMwLWEyNTEtZjA4MTIyM2NlODZi'

def get_user_push_time(deviceToken):
    now = timezone.localtime(timezone.now())
    config = AppConfig.objects.get(client=deviceToken)
    config_alertas = config.hora_alertas_verificacion.split(',')
    hora = int(config_alertas[0])
    minuto = int(config_alertas[1])
    if now.hour > hora:
        new_date = now.replace(hour=now.hour, minute=min(now.minute+2,59), second=0, microsecond=0)
    else:
        new_date = now.replace(hour=hora, minute=minuto, second=0, microsecond=0)
    if new_date < now:
        return timezone.make_naive(now.replace(minute=min(now.minute+1,59)), timezone.utc)
    else:
        naive_date = timezone.make_naive(new_date, timezone.utc)
        return naive_date

def prepare_push_time():
    now = timezone.localtime(timezone.now())
    new_date = now.replace(second=min(now.second+2,59), microsecond=0)
    naive_date = timezone.make_naive(new_date, timezone.utc)
    return naive_date

def get_headers():
    headers = {'X-Parse-Application-Id': Parse_Application_Id, 'X-Parse-REST-API-Key': Parse_REST_Key, 'content-type': 'application/json'}    
    return headers

def send_group_push(deviceToken, alert, sound=None, action=None, badge=None, push_time=None, expiration_time=None, group=None, other=None):
    if not deviceToken == 'admin':
        url = 'https://api.parse.com/1/push'
        data = {'alert':alert}
        if sound:
            data['sound'] = sound
        else:
            data['sound'] = " "
        if action:
            data['action'] = action
        if other:
            data['other'] = other
        if vehiculo:
            data['vehiculo'] = `int(vehiculo)`
        if badge:
            data['badge'] = 'Increment'
        if push_time == 'now':
            payload = {'where': {'channels':[group]}, 'data':data}
        elif not push_time:
            payload = {'where': {'channels':[group]}, 'push_time':get_user_push_time(deviceToken).isoformat()+'Z', 'data':data}
        else:
            payload = {'where': {'channels':[group]}, 'push_time':push_time.isoformat()+'Z', 'data':data}
        if expiration_time:
            payload['expiration_time'] = expiration_time.isoformat()+'Z'
        r = requests.post(url, data=json.dumps(payload), headers=get_headers())

def send_parse_push(deviceToken, alert, sound=None, action=None, badge=None, push_time=None, expiration_time=None, vehiculo=None, other=None, token=None):
    url = 'https://api.parse.com/1/push'
    data = {'alert':alert}
    if sound:
        data['sound'] = sound
    if action:
        data['action'] = action
    if other:
        data['other'] = other
    if vehiculo:
        data['vehiculo'] = `int(vehiculo)`
    if token:
        data['token'] = token
    if badge:
        data['badge'] = 'Increment'
    if push_time == 'now':
        payload = {'where': {'userToken':deviceToken}, 'data':data, 'push_time':prepare_push_time().isoformat()+'Z'}
    elif not push_time:
        payload = {'where': {'userToken':deviceToken}, 'push_time':get_user_push_time(deviceToken).isoformat()+'Z', 'data':data}
    else:
        payload = {'where': {'userToken':deviceToken}, 'push_time':push_time, 'data':data}
    if expiration_time:
        payload['expiration_time'] = expiration_time.isoformat()+'Z'
    r = requests.post(url, data=json.dumps(payload), headers=get_headers())

def send_push(deviceToken, alert, sound=None, action=None, badge=None, push_time=None, expiration_time=None, vehiculo=None, other=None, token=None):
    invalid_clients = ['admin','verifica','drivemee','web']
    if deviceToken not in invalid_clients:
        client = Client.objects.get(deviceToken=deviceToken)
        try:
            devices = client.device.all()
        except:
            devices = [client.device]
        for dev in devices:        
            if not dev.onesignal_token or dev.onesignal_token == '':
                send_parse_push(deviceToken, alert, sound, action, badge, push_time, expiration_time, vehiculo, other, token)
                return None
            url = 'https://onesignal.com/api/v1/notifications'
            contents = {'en':alert}
            player_id = [dev.onesignal_token]
            payload = {'app_id':OneSignal_App_Id, 'contents':contents, 'include_player_ids':player_id}
            data = {}
            if sound:
                payload['ios_sound'] = sound
                payload['android_sound'] = sound
            
            if badge:
                payload['ios_badgeType'] = 'Increase'
                payload['ios_badgeCount'] = 1
            
            if action:
                data['action'] = action
            
            if other:
                data['other'] = other
            
            if vehiculo:
                data['vehiculo'] = `int(vehiculo)`
            
            if token:
                data['token'] = token
            
            payload['data'] = data
            if not push_time:
                payload['send_after'] = get_user_push_time(deviceToken).isoformat()
            elif not push_time == 'now':
                payload['send_after'] = push_time
            r = requests.post(url, data=json.dumps(payload), headers=os_get_headers())
        return True

def send_targetted_push(tokenList, alert, push_time):
    url = 'https://api.parse.com/1/push'
    data = {'alert':alert}
    data['sound'] = ' '
    data['badge'] = 'Increment'
    payload = {'where': {'userToken':{'$in':tokenList}}, 'data':data, 'push_time':push_time.isoformat()+'Z'}
    r = requests.post(url, data=json.dumps(payload), headers=get_headers())
    return r

def send_mass_push(alert, sound=None, action=None, badge=None, push_time=None):
    url = 'https://api.parse.com/1/push'
    data = {'alert':alert}
    if sound:
        data['sound'] = sound
    if action:
        data['action'] = action
    if badge:
        data['badge'] = 'Increment'
    if push_time == 'now':
        payload = {'where': {'channels':'global'}, 'data':data}
    elif push_time:
        payload = {'where': {'channels':'global'}, 'push_time':push_time.isoformat()+'Z', 'data':data}
    else:
        payload = {'where': {'channels':'global'}, 'data':data}
    
    r = requests.post(url, data=json.dumps(payload), headers=get_headers())

def os_get_headers():
    headers = {'content-type': 'application/json'}    
    return headers

def os_get_auth_headers():
    headers = {'content-type': 'application/json', 'Authorization':'Basic '+OneSignal_REST_Key}    
    return headers

def os_send_targetted_push(tokenList, alert):
    url = 'https://onesignal.com/api/v1/notifications'
    contents = {'en':alert}
    payload = {'app_id':OneSignal_App_Id, 'contents':contents, 'include_player_ids':tokenList}
    payload['ios_sound'] = ' '
    payload['android_sound'] = ' '
    payload['ios_badgeType'] = 'Increase'
    payload['ios_badgeCount'] = 1
    r = requests.post(url, data=json.dumps(payload), headers=os_get_headers())
    return r

def os_send_mass_push(alert, sound=None, action=None, badge=None, push_time=None):
    url = 'https://onesignal.com/api/v1/notifications'
    contents = {'en':alert}
    payload = {'app_id':OneSignal_App_Id, 'contents':contents}
    payload['ios_sound'] = ' '
    payload['android_sound'] = ' '
    payload['ios_badgeType'] = 'Increase'
    payload['ios_badgeCount'] = 1
    payload['included_segments'] = ['All']    
    r = requests.post(url, data=json.dumps(payload), headers=os_get_auth_headers())
    return r

