# -*- coding: utf-8 -*- 
import requests
import json
#curl -X POST --data-urlencode 'payload={"channel": "#verifica", "username": "DjangoBot", "text": "This is posted to #verifica and comes from a bot named webhookbot.", "icon_emoji": ":taco:"}' https://hooks.slack.com/services/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

Slack_Webhook = 'https://hooks.slack.com/services/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'

def send_message(message='', channel='#verifica', username='DjangoBot', icon_emoji=None):
    url = Slack_Webhook
    payload= {'text':message, 'channel':channel, 'username':username, 'icon_emoji':icon_emoji}
    r = requests.post(url, data=json.dumps(payload))
