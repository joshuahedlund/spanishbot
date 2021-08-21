# -*- coding: utf-8 -*-
import datetime
import simplejson as json
import os
import random
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from urllib.request import urlopen

# instantiate Slack client
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

wotd_url = 'https://wotd.transparent.com/rss/es-widget.xml'

def get_weekday():
    WEEKDAYS = [
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo"
    ]
    weekdayint = datetime.datetime.today().weekday()
    return WEEKDAYS[weekdayint]

def get_greeting():
    GREETINGS = [
        '¡Hola! Hoy',
        'oye,'
    ]

    index = random.randint(0,1)
    return GREETINGS[index]

def get_html(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html

def get_tag(html, tag):
    start_index = html.find("<"+tag+">") + len("<"+tag+">")
    end_index = html.find("</"+tag+">")
    return html[start_index:end_index]

def post_slack(text, blocks):
    response = client.chat_postMessage(
        channel="#fam-español",
        text=text,
        blocks=blocks
    )
    return response

def build_blocks(greeting, word, translation, ex_spanish, ex_english):
    blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": greeting
                }
            },
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": "palabra del día / word of the day:"
    			}
    		},
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": ">*"+word+"*\n>_"+translation+"_"
    			}
    		},
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": "*\""+ex_spanish+"\"*\n_\""+ex_english+"\"_"
    			}
    		}
    	]
    return blocks

try:
    greeting = get_greeting() + " es " + get_weekday()
    html = get_html(wotd_url)

    word = get_tag(html, "word")
    translation = get_tag(html, "translation")
    ex_spanish = get_tag(html, "fnphrase")
    ex_english = get_tag(html, "enphrase")

    blocks = build_blocks(greeting, word, translation, ex_spanish, ex_english)

    #print(text)
    response = post_slack(greeting, blocks)

    #print(blocks)
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"]
  printf("Got an error: {e.response['error']}")