import logging
from slackbot.bot import respond_to, default_reply, listen_to
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


def get_channel_name(message: Message):
    if 'channel' not in message.body or \
            (not message.body['channel'].startswith('C') and not message.body['channel'].startswith('G')):
        logging.warning('failed to get channel name: %r' %message.body)
        return None
    try:
        channel_name = message._client.channels[message.body['channel']]['name']
    except KeyError:
        message._client.reconnect()
        channel_name = message._client.channels[message.body['channel']]['name']
    return channel_name


def get_username_by_id(message: Message, userid=None):
    if userid is None:
        if 'username' in message.body:
            return message.body['username']
        elif 'user' in message.body:
            userid = message.body['user']
        else:
            return 'unknown user'
    try:
        username = message._client.users[userid]['name']
    except KeyError:
        message._client.reconnect()
        username = message._client.users[userid]['name']
    return username


def send_wechat_file(group_name, filetype, file_path, slackmsg=None):
    groups = wxbot.groups().search(group_name)
    if groups:
        if filetype == 'mp4':
            groups[0].send_video(file_path)
        elif filetype in ['png', 'jpg', 'gif']:
            groups[0].send_image(file_path)
        else:
            groups[0].send_file(file_path)
    else:
        if slackmsg:
            slackmsg.reply('warning: wechat group not found: %s' % group_name)


def send_wechat_text(group_name, text, slackmsg=None):
    groups = wxbot.groups().search(group_name)
    if groups:
        groups[0].send_msg(text)
    else:
        if slackmsg:
            slackmsg.reply('warning: wechat group not found: %s' % group_name)


def filter_emoji(text):
    def func(match):
        emoji = match.groups()[0]
        if not emoji in config.emoji_map:
            return match.group()
        else:
            unified = config.emoji_map[emoji]
            return b''.join(b'\\U'+b'0'*(8-len(i))+i.encode('ascii') for i in unified.split('-')).decode('unicode-escape')
    p = r"\:([a-zA-Z0-9\-_\+]+)\:(?:\:([a-zA-Z0-9\-_\+]+)\:)?"
    return re.sub(p, func, text)


def filter_content(message: Message):
    content = message.body['text']
    def func(matchobj):
        return matchobj.group(1) + get_username_by_id(message, matchobj.group(2)) + matchobj.group(3)

    content = re.sub(r'(<@)(U[A-Z0-9]*)(>)', func, content)
    content = filter_emoji(content)
    return content


@respond_to('list')
def command_list(msg):
    msg.reply('all mappings(wechat <> slack): \n%s' % "\n".join(["%s <> %s"%(k,v) for (k, v) in config.wechat_slack_map.items()]))


@respond_to('status')
def command_status(msg):
    channel_name = get_channel_name(msg)
    if not channel_name:
        msg.reply('use this command in a channel')
    elif channel_name in config.slack_wechat_map:
        group_name = config.slack_wechat_map[channel_name]
        msg.reply('this channel is mapped to wechat group: %s' % group_name)
    else:
        msg.reply('this channel is not mapped to wechat group')


@respond_to('disable (.*)')
def command_disable(msg, group_name):
    group_name = group_name.strip()
    channel_name = get_channel_name(msg)
    if not channel_name:
        msg.reply('use this command in a channel')
    else:
        config.del_mapping(group_name=group_name, channel_name=channel_name)
        reply_content = "mapping disabled between %s <> %s" % (group_name, channel_name)
        msg.reply(reply_content)
        send_wechat_text(group_name, reply_content, msg)


@respond_to('sync (.*)')
def command_sync(msg: Message, group_name):
    group_name = group_name.strip()
    channel_name = get_channel_name(msg)
    if not channel_name:
        msg.reply('use this command in a channel')
    else:
        config.set_mapping(group_name=group_name, channel_name=channel_name)
        reply_content = 'mapping established between %s <> %s"' % (group_name, channel_name)
        msg.reply(reply_content)
        send_wechat_text(group_name, reply_content, msg)


@respond_to('help')
def my_default_hanlder(message):
    USAGE = '''
        @wechat sync <wechat group name>
        @wechat disable <wechat group name>
        @wechat status
        @wechat list
        @wechat help
    '''
    message.reply(USAGE)




@listen_to('.*')
def any_message(message: Message):
    try:
        logging.info(message.body)
        if message.body['type'] == 'message':
            channel_name = get_channel_name(message)
            username = get_username_by_id(message)
            logging.info("%s, %s", channel_name, username)
            if channel_name and channel_name in config.slack_wechat_map:
                group_name = config.slack_wechat_map[channel_name]
                send_wechat_text(group_name, username + ' said: ' + filter_content(message))
                if 'subtype' in message.body and message.body['subtype'] == 'file_share':
                    url = message.body['file']['url_private_download']
                    filetype = message.body['file']['filetype']
                    filepath = 'temp/slack_' + message.body['file']['id'] + "." + filetype
                    download_file(url, filepath)
                    send_wechat_file(group_name, filetype, filepath)
                else:
                    logging.error("group name not found in contacts: %s", group_name)
            else:
                pass
        else:
            logging.warning('unable to process the message')
    except Exception as e:
        logging.exception(e)

