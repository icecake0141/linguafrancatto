#!/usr/bin/env python3
import os
import json
import requests
from slack_sdk.rtm import RTMClient

# DeepL API
url = "https://api.deepl.com/v2/translate"
deepl_auth_key = os.environ["DEEPL_TOKEN"]

# Slack
slack_token = os.environ["SLACK_BOT_TOKEN"]

@RTMClient.run_on(event="message")
def print_message(**payload):

#deepl
    data = payload['data']
    web_client = payload['web_client']

    payload_req = {"auth_key":deepl_auth_key,"text":data['text'], "target_lang":"EN"}
    r = requests.get(url, params=payload_req)
    # printf debug
    print(r)
    x = json.loads(r.text)["translations"][0]["text"]
    y = payload['data']['client_msg_id']

    # post message to Slack
    channel_id = data['channel']
#    user = data['user'] 

    web_client.chat_postMessage(
        channel=channel_id,
#        text=print(x["translations"]["text"])
        text=x + y
    )

### just print
#    data = payload['data']
#    web_client = payload['web_client']
#    print(json.dumps(data, indent=4))

### default
#def say_hello(**payload):
    #data = payload['data']
    #web_client = payload['web_client']

    #if 'Hello' in data['text']:
        #channel_id = data['channel']
##        thread_ts = data['ts']
        #user = data['user'] # This is not username but user ID (the format is either U*** or W***)

        #web_client.chat_postMessage(
            #channel=channel_id,
            #text="Hi <@{user}>!",
##            thread_ts=thread_ts
        #)

rtm_client = RTMClient(token=slack_token)
rtm_client.start()
