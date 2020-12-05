#!/usr/bin/env python3
# coding: utf-8

# Linguafrancatto
# Slack Language translation bot powered by DeepL 
# icecake0141

# Reference
# https://github.com/slackapi/bolt-python/blob/main/examples/google_app_engine/flask/main.py

import json
import logging
import os
import re
import requests
import time
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

###  global variables
# Debug
DEBUG = os.environ.get("DEBUG_MODE")

# DeepL API
url = "https://api.deepl.com/v2/translate"
deepl_auth_key = os.environ.get("DEEPL_TOKEN")


############ Initialization ############
# Initializes your app with your bot token and signing secret
bolt_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)

# Debug
#logging.basicConfig(level=logging.DEBUG)

#@app.middleware  # or app.use(log_request)
#def log_request(logger, body, next):
    #logger.debug(body)
    #return next()

############ END Initialization ############

############ TEST ############

############ END TEXT ############

# Listens to incoming messages that contain "hello"
@bolt_app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(text=f"Hey there <@{message['user']}>!")

@bolt_app.message(":wave:")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")

@bolt_app.message("translate")
def translate(message, say):

    # Post DeepL API request
    payload_req = {"auth_key":deepl_auth_key,"text":message['text'], "target_lang":"EN"}
    r = requests.get(url, params=payload_req)

    translated_text = json.loads(r.text)["translations"][0]["text"]

    say(f"{translated_text}")

    time.sleep(1)

@bolt_app.message("")
def noop():
    return "", 200, {}


@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


# Start your app
if __name__ == "__main__":
    app.run(debug=DEBUG, port=int(os.environ.get("PORT", 3000)))