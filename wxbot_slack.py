#!/usr/bin/env python
# coding: utf-8

from wxbot import *

from slackbot.bot import SlackClient
import yaml

config = yaml.load(file('config.yaml').read())
wx_slack_map = config['bindings']
slack_client = SlackClient(config['slack_token'])


class WxBotSlack(WXBot):
    MSG_TYPE_GROUP = 3
    MSG_TYPE_CONTACT = 4

    CONTENT_TYPE_TEXT = 0
    CONTENT_TYPE_IMAGE = 3
    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == self.MSG_TYPE_GROUP:
            content_type = msg['content']['type']
            groupname = msg['user']['name']
            username = msg['content']['user']['name']
            if content_type == self.CONTENT_TYPE_TEXT:
                if groupname in wx_slack_map:
                    slack_client.send_message(wx_slack_map[groupname], username + " said: " + msg['content']['desc'])
            elif content_type == self.CONTENT_TYPE_IMAGE:
                # todo
                pass
            else:
                # not supported
                pass


wxbot = WxBotSlack()
