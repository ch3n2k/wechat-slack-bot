import logging
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re

import slackbot.bot as bot
from slackbot.dispatcher import Message
from slackbot.slackclient import Channel

from wxbot_slack import wxbot
import requests
import config


class FileDownloadException(Exception): pass


def download_file(url, filepath):
    resp = requests.get(url, headers={'Authorization': 'Bearer ' + config.slack_token})
    if resp.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(resp.content)
    else:
        raise FileDownloadException()


def handle_command(command, channel_name):
    USAGE = '''!wechat sync <wechat group name>
!wechat disable <wechat group name>
'''

    if not command.startswith("!wechat"):
        return

    params = command.split()
    if len(params) < 3:
        return "bad usage. \n" + USAGE
    action = params[1]
    remainings = command[command.find(action) + len(action):].strip()
    if action == 'sync':
        config.set_mapping(group_name=remainings, channel_name=channel_name)
        return "mapping established between %s <> %s" % (remainings, channel_name)
    elif action == 'disable':
        config.del_mapping(group_name=remainings, channel_name=channel_name)
        return "mapping disabled between %s <> %s" % (remainings, channel_name)
    else:
        return "bad usage. \n" + USAGE

    
@listen_to('.*')
def any_message(message: Message):
    try:
        logging.info(message.body)
        if message.body['type'] == 'message':
            try:
                channel_name = message._client.channels[message.body['channel']]['name']
            except KeyError:
                message._client.reconnect()
                channel_name = message._client.channels[message.body['channel']]['name']
            username = message._client.users[message.body['user']]['name']
            logging.info("%s, %s", channel_name, username)
            content = message.body['text']
            if content.startswith('!wechat'):
                reply = handle_command(content, channel_name)
                message.reply(reply)
                if channel_name in config.slack_wechat_map:
                    group_name = config.slack_wechat_map[channel_name]
                    groups = wxbot.groups().search(group_name)
                    if groups:
                        groups[0].send_msg(reply)
            elif channel_name in config.slack_wechat_map:
                group_name = config.slack_wechat_map[channel_name]
                groups = wxbot.groups().search(group_name)
                if groups:
                    groups[0].send_msg(username + ' said: ' + content)
                    if 'subtype' in message.body and message.body['subtype'] == 'file_share':
                        url = message.body['file']['url_private_download']
                        filename = 'slack_' + message.body['file']['id'] + "." + message.body['file']['filetype']
                        filepath = "temp/" + filename
                        download_file(url, filepath)
                        groups[0].send_image(filepath)
                else:
                    logging.error("group name not found in contacts: %s", group_name)
            else:
                pass
        else:
            logging.warning('unable to process the message')
    except Exception as e:
        logging.exception(e)

