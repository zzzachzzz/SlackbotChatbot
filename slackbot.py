"""
Slack chat-bot Lambda handler.
"""

import os
import logging
import urllib
import re
import random


BOT_TOKEN = os.environ["BOT_TOKEN"]
SLACK_URL = "https://slack.com/api/chat.postMessage"


def handle_text(text):
    if re.search(r'@UDPL13YSE', text, re.I):
        return ":loading:"
    if re.search(r'scrum', text, re.I):
        return "Yes! Gather my WEM minions! :wem_cult_member:"
    if re.search(r':punchbaby:|punch babies|punch baby', text, re.I):
        return "Praise WEM! :darkestwem:"
    if re.search(r'11|eleven', text, re.I):
        responses = ("The Dark Hour of WEM approaches",
                     "Ah 11, my favorite time of the day")
        return random.choice(responses)
    return None


def slackbot_response(slack_event):
    if "subtype" in slack_event:
        if slack_event['subtype'] == "slackbot_response":
            return True
    return False


def lambda_handler(data, context):
    # Grab the Slack event data.
    slack_event = data['event']

    # If message is from slackbot or another bot, ignore the Slack event.
    if "bot_id" in slack_event or slackbot_response(slack_event):
        logging.warn("Ignore bot event")
    else:
        text = slack_event["text"]
        message = handle_text(text)
        if message is None:
            return "200 OK"
        
        # Get the ID of the channel where the message was posted.
        channel_id = slack_event["channel"]

        # Create an associative array and URL-encode it, 
        # since the Slack API doesn't not handle JSON.
        data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", channel_id),
                ("text", message)
            )
        )
        data = data.encode("ascii")
        
        # Construct the HTTP request that will be sent to the Slack API.
        request = urllib.request.Request(
            SLACK_URL, 
            data=data, 
            method="POST"
        )
        # Add a header mentioning that the text is URL-encoded.
        request.add_header(
            "Content-Type", 
            "application/x-www-form-urlencoded"
        )
        # Fire off the request!
        urllib.request.urlopen(request).read()

    # Everything went fine.
    return "200 OK"
