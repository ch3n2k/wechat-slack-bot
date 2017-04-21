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
    '[Sob]': u'\U0001f62d',
    '[Shy]': u'\U0000263a',
    '[Shutup]': u'\U0001f64a',
    '[Sleep]': u'\U0001f634',
    '[Cry]': u'\U0001f623',
    '[Awkward]': u'\U0001f630',
    '[Pout]': u'\U0001f621',
    '[Wink]': u'\U0001f61c',
    '[Grin]': u'\U0001f601',
    '[Surprised]': u'\U0001f631',
    '[Frown]': u'\U0001f62f',
    '[Scream]': u'\U0001f62b',
    '[Joyful]': u'\U0001f60a',
    '[Smug]': u'\U0001f615',
    '[Drowsy]': u'\U0001f62a',
    '[Panic]': u'\U0001f631',
    '[Sweat]': u'\U0001f613',
    '[Laugh]': u'\U0001f604',
    '[Loafer]': u'\U0001f60f',
    '[Strive]': u'\U0001f4aa',
    '[Scold]': u'\U0001f624',
    '[Doubt]': u'\U00002753',
    '[Dizzy]': u'\U0001f632',
    '[Skull]': u'\U0001f480',
    '[Relief]': u'\U0001f625',
    '[Clap]': u'\U0001f44f',
    '[Trick]': u'\U0001f47b',
    '[Bah！L]': u'\U0001f63e',
    '[Bah！R]': u'\U0001f63e',
    '[Yawn]': u'\U0001f62a',
    '[Lookdown]': u'\U0001f612',
    '[Puling]': u'\U0001f614',
    '[Sly]': u'\U0001f608',
    '[Kiss]': u'\U0001f618',
    '[Cleaver]': u'\U0001f52a',
    '[Melon]': u'\U0001f349',
    '[Beer]': u'\U0001f37a',
    '[Coffee]': u'\U00002615',
    '[Pig]': u'\U0001f437',
    '[Rose]': u'\U0001f339',
    '[Lip]': u'\U0001f48b',
    '[Heart]': u'\U00002764',
    '[BrokenHeart]': u'\U0001f494',

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
