#!/usr/bin/env python
# coding: utf-8

from wxbot import *

from slackbot.bot import SlackClient
import config
import logging
import urlparse
import re

emoji_map_table = {
    '[Smile]': u'\U0001f600',
    '[Drool]': u'\U0001f60d',
    '[Scowl]': u'\U0001f633',
    '[Chill]': u'\U0001f60e',
}


def filter_text(text):
    for k, v in emoji_map_table.iteritems():
        text = text.replace(k, v)
    while True:
        result = re.search('(<span class="emoji emoji([0-9a-f]*)"></span>)', text)
        if result:
            emoji = result.groups()[1]
            text = text.replace(result.groups()[0], ('\\U' + '0' * (8 - len(emoji)) + emoji).decode('unicode-escape'))
        else:
            break
    return text


class WxBotSlack(WXBot):
    MSG_TYPE_GROUP = 3
    MSG_TYPE_CONTACT = 4

    CONTENT_TYPE_TEXT = 0
    CONTENT_TYPE_IMAGE = 3

    def __init__(self):
        WXBot.__init__(self)
        self.slack_client = SlackClient(config.slack_token)

    def handle_msg_all(self, msg):
        try:
            if msg['msg_type_id'] == self.MSG_TYPE_GROUP:
                content_type = msg['content']['type']
                groupname = msg['user']['name']
                username = filter_text(msg['content']['user']['name'])
                content = filter_text(msg['content']['desc'])
                logging.info("%s, %s, %s", content_type, groupname, username)
                if groupname in config.wechat_slack_map:
                    channelname = config.wechat_slack_map[groupname]
                    if content_type == self.CONTENT_TYPE_TEXT:
                        self.slack_client.send_message(channelname, username + " said: " + content)
                    elif content_type == self.CONTENT_TYPE_IMAGE:
                        logging.info("image content data: %r", msg['content']['data'])
                        filename = 'img_' + urlparse.parse_qs(urlparse.urlparse(msg['content']['data']).query)['MsgID'][
                            0] + '.jpg'
                        filepath = 'temp/' + filename
                        comment = username + " sent a image: " + filename
                        self.slack_client.upload_file(channelname, filename, filepath, comment)
                    else:
                        # todo: handle other message content types
                        pass
                    if username == 'unknown':
                        self.get_contact()
                else:
                    pass

        except Exception, e:
            logging.exception(e)


wxbot = WxBotSlack()
