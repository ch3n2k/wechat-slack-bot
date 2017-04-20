#!/usr/bin/env python
# coding: utf-8

from wxbot import *

from slackbot.bot import SlackClient
import yaml
import logging
import urlparse
import re

config = yaml.load(file('config.yaml').read())
wx_slack_map = config['bindings']
slack_client = SlackClient(config['slack_token'])
logging.info("group mapping configuration:")
for k,v in wx_slack_map.iteritems():
    logging.info("%s <> %s", k, v)

emoji_map_table = {
    '[Smile]': u'\U0001f600',
    '[Drool]': u'\U0001f60d',
}

def filter_text(text):
    for k, v in emoji_map_table.iteritems():
        text = text.replace(k, v)
    while True:
        result = re.search('(<span class="emoji emoji([0-9a-f]*)"></span>)', text)
        if result:
            emoji = result.groups()[1]
            text = text.replace(result.groups()[0], ('\\U' + '0' * (8-len(emoji)) + emoji).decode('unicode-escape'))
        else:
            break
    return text

class WxBotSlack(WXBot):
    MSG_TYPE_GROUP = 3
    MSG_TYPE_CONTACT = 4

    CONTENT_TYPE_TEXT = 0
    CONTENT_TYPE_IMAGE = 3
    def handle_msg_all(self, msg):
      try:
        if msg['msg_type_id'] == self.MSG_TYPE_GROUP:
            content_type = msg['content']['type']
            groupname = msg['user']['name']
            username = msg['content']['user']['name']
            logging.info("%s, %s, %s", content_type, groupname, username)
            if groupname in wx_slack_map:
                channelname = wx_slack_map[groupname]
                if content_type == self.CONTENT_TYPE_TEXT:
                    slack_client.send_message(channelname, username + " said: " + filter_text(msg['content']['desc']))
                elif content_type == self.CONTENT_TYPE_IMAGE:
                    logging.info("image content data: %r", msg['content']['data'])
                    filename = 'img_' + urlparse.parse_qs(urlparse.urlparse(msg['content']['data']).query)['MsgID'][0] + '.jpg'
                    filepath = 'temp/' + filename
                    comment = username + " sent a image: " + filename
                    slack_client.upload_file(channelname, filename, filepath, comment)
                else:
                    #todo
                    pass
                if username == 'unknown':
                    self.get_contact()
            else:
                # not in the mapping
                pass

      except Exception, e:
        logging.exception(e)

wxbot = WxBotSlack()
