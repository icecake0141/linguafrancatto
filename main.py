#!/usr/bin/env python3
# coding: utf-8

# Linguafrancatto
# Language translation bot powered by DeepL for Slack
# icecake0141

### import
import os
import logging
import re
import json
import time
import pprint
import requests
from flask import Flask
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError

#from slack_sdk.rtm import RTMClient

# entrypoint
app = Flask(__name__)
#slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

client = WebClient()
api_response = client.api_test()

###
### Functions

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

# handy time printer
#def get_time():
  #localtime = time.localtime()
  #result = time.strftime("%I:%M:%S %p", localtime)
  #return result

# report message to guardian
#def report_to_guardian(text, payload):

    #web_client = payload['web_client']
    #channel_id = web_client.conversations_open(users=guardian_uid)['channel']['id']

    #web_client.chat_postMessage(
        #channel = channel_id,
        #text = text
    #)

###
### RTM event functions

# When an API request is accepted
# Get and store bot's ID and name
#@RTMClient.run_on(event="open")
#def bot_initialization(**payload):

    ## import event data
    #data = payload['data']

    #text = json.dumps(pprint.pformat(data))
    #report_to_guardian(text, payload)

    #global myid
    #myid = data['self']['id']
    #global myname
    #myname = data['self']['name']


# When connection to a slack space is established
# Report to a guardian
#@RTMClient.run_on(event="hello")
#def report_status_after_connection(**payload):

    #text = "Hello, " + myname + " is up and running. " + get_time()

    #report_to_guardian(text, payload)


# When a new message is posted
#@RTMClient.run_on(event="message")
#@slack_events_adapter.on("message")
#def translate_message(**payload):

    #client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

    #try:
        #response = client.chat_postMessage(channel='#random', text="Hello world!")
        #assert response["message"]["text"] == "Hello world!"
    #except SlackApiError as e:
        ## You will get a SlackApiError if "ok" is False
        #assert e.response["ok"] is False
        #assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        #print(f"Got an error: {e.response['error']}")

    ## import event data
    #event = payload.get['event',{}]

    ## Exit if the message is from any bots
    #if 'subtype' in event:
        #if event['subtype'] == 'bot_message':
            #return

    ## import slack API info
    #web_client = payload['web_client']

    #if re.search('にゃん',data['text']) :
        #tr_to_lang = 'EN'
    #elif re.search('Meow',data['text']) :
        #tr_to_lang = 'JA'
    #elif re.search('Miaou',data['text']) :
        #tr_to_lang = 'JA'
    #elif re.search('мяу',data['text']) :
        #tr_to_lang = 'JA'
    #else:
        #return

    ## Post DeepL API request
    #payload_req = {"auth_key":deepl_auth_key,"text":data['text'], "target_lang":tr_to_lang}
    #r = requests.get(url, params=payload_req)

    ## debug
    #text = json.dumps(pprint.pformat(r.text))
    #report_to_guardian(text, payload)

    #translated_text = json.loads(r.text)["translations"][0]["text"]
    #original_message_id = payload['data']['client_msg_id']

    ## post message to Slack
    #channel_id = data['channel']
    #user_id = data['user']
    #user_name = web_client.users_info(
        #user = user_id
    #)['user']['name']

    #message = 'In message ' + original_message_id + ', ' + user_name + ' said:\n'
    #message += translated_text

    #web_client.chat_postMessage(
        #channel = channel_id,
        #text = message
    #)
    #time.sleep(1)

###
### main
if __name__ == "__main__":

    ###  global variables
    # DeepL API
    #url = "https://api.deepl.com/v2/translate"
    #deepl_auth_key = os.environ["DEEPL_TOKEN"]

    # Slack
    #slack_token = os.environ["SLACK_BOT_TOKEN"]
    #guardian_uid = os.environ["GUARDIAN_UID"]

    # bot name/id
    #myid = ""
    #myname = ""

    # module logging
    # Logging package for Python. Based on PEP 282 and comments thereto in comp.lang.python.
    # To use, simply 'import logging' and log away!
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # class StreamHandler(stream: Optional[IO[str]]=...)
    # A handler class which writes logging records, appropriately formatted,
    # to a stream. Note that this class does not close the stream, as sys.stdout
    # or sys.stderr may be used.
    logger.addHandler(logging.StreamHandler())

    app.run(host='0.0.0.0', port=8080, debug=True)

    # Create a RTM client license
#    rtm_client = RTMClient(token=slack_token)

    # Establish a WebSocket connection with Slack.
#    rtm_client.start()
