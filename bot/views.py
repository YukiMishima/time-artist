from django.shortcuts import render
from django.http import HttpResponse
from bot.load_serif import serif

import json
import random
import requests

def index(request):
    return HttpResponse("This is bot api.")

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'sUNmF6Y6hPssxRd1kjU+SEA+9yfaDfpAfbPvYhGZyvbI4nM37NgzMti/tchb1vinqH8oybkxzEaEJ9oQ+Fg0euIX/RJ3Gu1S2nvzdesqm3F3ml0NRy3/0S2gZnumweMsCFOsFDEcYZwTuZD8Xy4wMgdB04t89/1O/w1cDnyilFU='

HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def reply_text(reply_token, text):
    # serif = open("bot/serif.txt","r",'utf-8').read().split("\n")
    reply = random.choice(serif)
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

def callback(request):
    reply=""
    request_json = json.loads(request.body.decode('utf-8'))
    for e in request_json['events']:
        reply_token=['replyToken']
        message_type = e['message']['type']

        if message_type == 'text':
            text = e['message']['text']
            reply += reply_text(reply_token, text)
    return HttpResponse(reply)