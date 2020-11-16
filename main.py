#!/usr/bin/env python3
# coding: utf-8

# Linguafrancatto
# Language translation bot powered by DeepL for Slack

### import
import os
import re
import json
import requests
import time
import pprint
#from pprint import pprint
from slack_sdk.rtm import RTMClient

###  global variables
# DeepL API
url = "https://api.deepl.com/v2/translate"
deepl_auth_key = os.environ["DEEPL_TOKEN"]

# Slack
slack_token = os.environ["SLACK_BOT_TOKEN"]
guardian_uid = os.environ["GUARDIAN_UID"]

# bot name/id
myid = ""
myname = ""

###
### Functions

# handy time printer
def get_time():
  localtime = time.localtime()
  result = time.strftime("%I:%M:%S %p", localtime)
  return result

# report message to guardian
def report_to_guardian(text, payload):

    web_client = payload['web_client']
    channel_id = web_client.conversations_open(users=guardian_uid)['channel']['id']

    web_client.chat_postMessage(
        channel = channel_id,
        text = text
    )

###
### RTM event functions

# When an API request is accepted
# Get and store bot's ID and name
@RTMClient.run_on(event="open")
def bot_initialization(**payload):

    # import event data
    data = payload['data']

    text = json.dumps(pprint.pformat(data))
    report_to_guardian(text, payload)

    global myid
    myid = data['self']['id']
    global myname
    myname = data['self']['name']


# When connection to a slack space is established
# Report to a guardian
@RTMClient.run_on(event="hello")
def report_status_after_connection(**payload):

    text = "Hello, " + myname + " is up and running. " + get_time()

    report_to_guardian(text, payload)


# When a new message is posted
@RTMClient.run_on(event="message")
def translate_message(**payload):

    # import event data
    data = payload['data']

    # Exit if the message is from any bots
    if 'subtype' in data:
        if data['subtype'] == 'bot_message':
            return

    # import slack API info
    web_client = payload['web_client']

    if re.search('にゃん',data['text']) :
        tr_to_lang = 'EN'
    elif re.search('Meow',data['text']) :
        tr_to_lang = 'JA'
    elif re.search('Miaou',data['text']) :
        tr_to_lang = 'JA'
    elif re.search('мяу',data['text']) :
        tr_to_lang = 'JA'
    else:
        return

    # Post DeepL API request
    payload_req = {"auth_key":deepl_auth_key,"text":data['text'], "target_lang":tr_to_lang}
    r = requests.get(url, params=payload_req)

    # debug
    text = json.dumps(pprint.pformat(r.text))
    report_to_guardian(text, payload)

    translated_text = json.loads(r.text)["translations"][0]["text"]
    original_message_id = payload['data']['client_msg_id']

    # post message to Slack
    channel_id = data['channel']
    user_id = data['user']
    user_name = web_client.users_info(
        user = user_id
    )['user']['name']

    message = 'In message ' + original_message_id + ', ' + user_name + ' said:\n'
    message += translated_text

    web_client.chat_postMessage(
        channel = channel_id,
        text = message
    )
    time.sleep(1)

###
### main

# Create a RTM client license
rtm_client = RTMClient(token=slack_token)

# Establish a WebSocket connection with Slack.
rtm_client.start()

#rtm_client.stop()