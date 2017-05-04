#!/usr/bin/env python
# coding: utf-8

#import gevent.monkey
#gevent.monkey.patch_all()

import yaml
import logging
logging.basicConfig(level=logging.INFO)
import slackbot.settings
slackbot.settings.PLUGINS = [
    'slackbot_wechat_plugin',
]
slackbot.settings.API_TOKEN = yaml.load(open('config.yaml').read())['slack_token']
from slackbot.bot import Bot as SlackBot

from wxbot_slack import wxbot
from wxpy import embed

def wxbot_main():
    embed()


def slackbot_main():
    slackbot = SlackBot()
    slackbot.run()

if __name__ == '__main__':
    slackbot_main()
    #wxbot_main()


