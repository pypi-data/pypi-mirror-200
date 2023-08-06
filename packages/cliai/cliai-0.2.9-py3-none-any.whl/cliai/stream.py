#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import requests
import sseclient

API_KEY = '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'
API_BASE = 'https://api.openai.com/v1/chat/completions'

req_headers = {
        'Accept': 'text/event-stream',
        'Authorization': 'Bearer ' + API_KEY
    }

req_body = {
      "model": "gpt-3.5-turbo",
      "messages": [{'role': 'user',
                    'content': 'hello'}],
      "max_tokens": 100,
      "temperature": 1,
      "stream": True,
    }


req = requests.post(API_BASE,
                    stream=True,
                    headers=req_headers,
                    json=req_body)

client = sseclient.SSEClient(req.content)
for event in client.events():
    if event.data != '[Done]':
        print(json.loads(event.data)['choices'][0]['message']['content'], end="", flush=True)
