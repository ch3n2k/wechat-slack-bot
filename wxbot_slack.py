#!/usr/bin/env python3
# coding: utf-8

import wxpy
from slackbot.bot import SlackClient
import config
import logging
import re
from slackbot_main import slackbot

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
    u'[Bah！L]': u'\U0001f63e',
    u'[Bah！R]': u'\U0001f63e',
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
    '[Cake]': u'\U0001f382',
    '[Bomb]': u'\U0001f4a3',
    '[Poop]': u'\U0001f4a9',
    '[Moon]': u'\U0001f319',
    '[Sun]': u'\U0001f31e',
    '[Strong]': u'\U0001f44d',
    '[Weak]': u'\U0001f44e',
    '[Victory]': u'\U0001f31e',
    '[Fist]': u'\U0000270a',
    '[OK]': u'\U0001f44c',

}


def filter_text(text):
    for k, v in emoji_map_table.items():
        text = text.replace(k, v)
    while True:
        result = re.search('(<span class="emoji emoji([0-9a-f]*)"></span>)', text)
        if result:
            emoji = result.groups()[1]
            text = text.replace(result.groups()[0], ('\\U' + '0' * (8 - len(emoji)) + emoji).decode('unicode-escape'))
        else:
            break
    return text


wxbot = wxpy.Bot(console_qr=True, cache_path=True)
slack_client = slackbot._client


def forward_msg_to_slack(msg, channelname):
    username = msg.member.name
    if msg.type == wxpy.TEXT:
        content = filter_text(msg.text)
        slack_client.send_message(channelname, username + " said: " + content)
    elif msg.type == wxpy.PICTURE:
        filepath = "temp/" + msg.file_name
        data = msg.get_file(filepath)
        logging.info("image content data: %r", data)
        comment = username + " sent a image: " + msg.file_name
        slack_client.upload_file(channelname, msg.file_name, filepath, comment)
    elif msg.type == wxpy.VIDEO:
        filepath = "temp/" + msg.file_name
        data = msg.get_file(filepath)
        comment = username + " sent a video: " + msg.file_name
        slack_client.upload_file(channelname, msg.file_name, filepath, comment)
    else:
        pass


@wxbot.register(wxpy.Group)
def handle_msg_all(msg: wxpy.Message):
    try:
        logging.info("%r %r", msg.sender.name, msg.member.name)
        groupname = msg.sender.name
        if groupname in config.wechat_slack_map:
            channelname = config.wechat_slack_map[groupname]
            forward_msg_to_slack(msg, channelname)
        if msg.is_at and hasattr(config, 'botadmin'):
            forward_msg_to_slack(msg, '@' + config.botadmin)

    except Exception as e:
        logging.exception(e)
