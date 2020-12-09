#!/usr/bin/env python3
# coding: utf-8

# Linguafrancatto v2.1
# Slack Language translation bot powered by DeepL / Slack Bolt SDK
# icecake0141 / 2020
# https://github.com/icecake0141/linguafrancatto 

import json
import logging
import os
import re
import requests
import time
from flask import Flask, request
from slack_bolt import App, Ack
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

##################################
# Google App Engie debugger
# Enable this if you want to debug on GaE
#try:
#    import googleclouddebugger
#    googleclouddebugger.enable(
#        breakpoint_enable_canary=False
#    )
#except ImportError:
#    pass


############
###  global variables
# Debug
DEBUG = os.environ.get("DEBUG_MODE")

# DeepL API
url = "https://api.deepl.com/v2/translate"
url_usage = "https://api.deepl.com/v2/usage"
deepl_auth_key = os.environ.get("DEEPL_TOKEN")
#formality =os.environ.get("FORMALITY")


############
############ Initialization ############
# Initializes your app with your bot token and signing secret
bolt_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Instanciate WebClient
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

# Instanciate WebClient
app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)

# Slack
# multi channel translation
list_channel_basename = os.environ.get("MULTI_CHANNEL").split(",")

# retrieve channel object from Slack API
try:
    # Call the conversations.list method using the built-in WebClient
    channels = client.conversations_list()['channels']

except SlackApiError as e:
    logging.error("Error fetching conversations: {}".format(e))
    #logger.error("Error fetching conversations: {}".format(e))

name_dict, id_dict = {},{}
for i in channels:
    name_dict[i['name']] = i['id']
    id_dict[i['id']] = i['name']
# not good way :(
del i

# Logging
if DEBUG == "True":
    logging.basicConfig(level=logging.DEBUG)

############ END Initialization ############
############

############
############ Function ############

### DeepL ###
# Post DeepL translation API request
def deepl(text, tr_to_lang):

    # Hit text translation API
    payload_req = {"auth_key":deepl_auth_key,"text":text, "target_lang":tr_to_lang, "tag_handling":"xml"}
    r = requests.get(url, params=payload_req)

    translated_text = json.loads(r.text)["translations"][0]["text"]

    return translated_text


def deepl_usage():

    # Hit usage report API
    payload_req = {"auth_key":deepl_auth_key}
    r = requests.get(url_usage, params=payload_req)

    count = json.loads(r.text)["character_count"]
    limit = json.loads(r.text)["character_limit"]

    return count, limit

### Text manipulation ###
def replace_markdown(text_block):
    
    for i in text_block.readline():
        result 

    return result 

def revert_markdown(text_block):
    return result

### END Text manipulation ###

### Slack ###

############ END Functions ############
############

############
############ Bolt handlers ############


@bolt_app.message("Meousage")
def usage(ack:Ack, message, say):
    ack()

    # Check DeepL usage
    count, limit = deepl_usage()

    # Post DeepL API usage
    say(f"{count} characters translated so far in the current billing purriod.\n"\
        + f"Current meowximum number of characters that can be translated per billing purriod is {limit}.\n"\
        + f"{count/limit*100:.2f} % used.")
    say("Translation keyword:\n    Nyan:JP\n    Meow:EN\n    Miaou:FR\n    Мяу:RU")

    time.sleep(1)


@bolt_app.message(re.compile("(Nyan|Meow|Miaou|Мяу)"))
def ondemand_translate(ack: Ack, message, say, context):
    ack()

    # Determine target language to be translated
    if re.match("Nyan",context['matches'][0]) :
        tr_to_lang = "JA"
    elif re.match("Meow",context['matches'][0]) :
        tr_to_lang = "EN"
    elif re.match("Miaou",context['matches'][0]) :
        tr_to_lang = "FR"
    elif re.match("Мяу",context['matches'][0]) :
        tr_to_lang = "RU"
    else:
        return

    # Hit translation API
    translated_text = deepl(message['text'],tr_to_lang)

    # retrieve username from userid
    speaker = client.users_info(user=message['user']).data['user']['name']

    # Post message
    say(f"{speaker} said:\n{translated_text}")

    time.sleep(1)


@bolt_app.event('message', subtype('channel_join')
def

# catcher for multichannel translation
@bolt_app.event({"type": "message", "subtype": None})
def multichannel_translate(ack: Ack, message, say):
    ack()

    # Convert channel ID to channel name
    channelname = id_dict[message['channel']]

    # list_channel_basename contains a list of basename ("foobar" of foobar_en/foobar_fr/foobar) of channels,
    # where all conversations should be translated automatically.
    for channel_basename in list_channel_basename:
        # Check if the message is posted on specific channel name
        if re.search(channel_basename, channelname):
            # retrieve username from userid
            speaker = client.users_info(user=message['user']).data['user']['name']
            # if it receives a message from designated channel, it populate translated messages to remaining channels
            for i in name_dict:
                # skip if channel names are the same = it is the channel the message was originally posted
                if i == channelname:
                    pass
                # determine translation target language based on suffix of chanel name (_en/_fr/nothing=jp)
                elif re.search(channel_basename,i):
                    if re.search("-en$",i):
                        tr_to_lang = "EN"
                    elif re.search("-fr$",i):
                        tr_to_lang = "FR"
                    elif re.match(channel_basename,i):
                        tr_to_lang = "JA"
                    else:
                        continue
                    # Hit translation API
                    translated_text = deepl(message['text'],tr_to_lang)
                    # Post message
                    say(channel=name_dict[i],text=f"{speaker} said:\n{translated_text}")
                else:
                    pass

            time.sleep(1)
            return
        # if not, do nothing since it is not a target channel of translation
        else:
            return


#@bolt_app.message("")
#def catch_all(message):


@bolt_app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()


# error handling
@bolt_app.error
def custom_error_handler(error, body, logger):
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")

############ END Bolt handlers ############
############

############
############ Flask routes ############

# Call bolt handler
@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


## Handle your warmup logic here, e.g. set up a database connection pool
#@app.route("/_ah/warmup")
#def warmup(ack:Ack):
    #ack()

    #return "", 200, {}


@app.route("/_ah/start")
def spinup():

    # Google App Engine
    return "", 200, {}


@app.route("/_ah/stop")
def spindown():

    # Google App Engine
    return "", 200, {}

############ END Flask routes ############
############

############
############ MAIN ############
if __name__ == "__main__":

    app.run(debug=os.environ.get("DEBUG_MODE"), port=int(os.environ.get("PORT", 3000)))