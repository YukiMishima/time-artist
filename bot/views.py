from django.shortcuts import render
from django.http import HttpResponse
from bot.load_serif import serif
from api.models import Log

import json
import random
import requests
import datetime

def index(request):
    return HttpResponse("This is bot api.")

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'sUNmF6Y6hPssxRd1kjU+SEA+9yfaDfpAfbPvYhGZyvbI4nM37NgzMti/tchb1vinqH8oybkxzEaEJ9oQ+Fg0euIX/RJ3Gu1S2nvzdesqm3F3ml0NRy3/0S2gZnumweMsCFOsFDEcYZwTuZD8Xy4wMgdB04t89/1O/w1cDnyilFU='

HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def callback(request):
    reply=""
    request_json = json.loads(request.body.decode('utf-8'))
    for e in request_json['events']:
        reply_token=e['replyToken']
        message_type = e['message']['type']

        if message_type == 'text':
            text = e['message']['text']
            reply += reply_text(reply_token, text)
    return HttpResponse(reply)

def reply_text(reply_token, text):
    # reply = random.choice(serif)
    data = Log.objects.values('created_at','temperature')
    newest_data = str(int(data.last()['temperature']))
    newest_time = data.last()['created_at'].strftime("%Y{0}%M{1}%d{2}%H:%M:%S").format(*'年月日')
    reply = newest_time + 'の時点では' + newest_data + '%だワン'
    payload = {
        "replyToken": reply_token,
        "messages":[
            {
                "type":"text",
                "text":reply
            }
        ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload))
    return reply

def congestion(request):
    data = Log.objects.values('created_at','temperature')
    newest_congestion = data.last()['temperature']
    newest_time = data.last()['created_at'].strftime("%Y{0}%M{1}%d{2} %H:%M:%S").format(*'年月日')
    data_dict = {
        'title': 'test',
        'val': data,
        'newest_data': newest_congestion,
        'newest_time': newest_time,
    }
    return render(request, 'data.html', data_dict)