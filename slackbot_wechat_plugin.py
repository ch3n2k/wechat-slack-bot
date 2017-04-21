import logging
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re

import slackbot.bot as bot
from slackbot.dispatcher import Message
from slackbot.slackclient import Channel

from wxbot_slack import wxbot
import yaml
import requests

def html_escape(s):
    s = s.replace("&", "&amp;")
    s = s.replace(">", "&gt;")
    s = s.replace("<", "&lt;")
    s = s.replace('"', "&quot;")
    s = s.replace("'", "&apos;")
    return s
        
config = yaml.load(file('config.yaml').read())
slack_wechat_map = dict((x, html_escape(w)) for w, x in config['bindings'].iteritems())
logging.info( "channel mapping configuration:")
for k, v in slack_wechat_map.iteritems():
    logging.info("%s <> %s", k, v )

class FileDownloadException(Exception): pass

def download_file(url, filepath):
    resp = requests.get(url, headers={'Authorization': 'Bearer ' + config['slack_token']})
    if resp.status_code == 200:
        with file(filepath, 'w') as f:
            f.write(resp.content)
    else:
        raise FileDownloadException()
        
    
@listen_to('.*')
def any_message(message):
    try:
        logging.info(message.body)
        if message.body['type'] == 'message':
            channel_name = message.channel._client.channels[message.body['channel']]['name']
            username = message.channel._client.users[message.body['user']]['name']
            logging.info("%s, %s", channel_name, username)
            if channel_name in slack_wechat_map:
                group_name = slack_wechat_map[channel_name]
                group_id = wxbot.get_user_id(group_name)
                if group_id is not None:
                    wxbot.send_msg_by_uid(username + ' said: ' + message.body['text'], group_id)
                    if 'subtype' in message.body and message.body['subtype'] == 'file_share':
                        url = message.body['file']['url_private_download']
                        filename = 'slack_' + message.body['file']['id'] + "." + message.body['file']['filetype']
                        filepath = "temp/" + filename
                        download_file(url, filepath)
                        wxbot.send_img_msg_by_uid(filepath, group_id)
                else:
                    logging.error("group name not found in contacts: %s", group_name)
        else:
            logging.warning('unable to process the message')
    except Exception, e:
        logging.exception(e)

'''@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply('I can understand hi or HI!')
    # react with thumb up emoji
    message.react('+1')

@respond_to('I love you')
def love(message):
    message.reply('I love you too!')

@listen_to('Can someone help me?')
def help(message):
    # Message is replied to the sender (prefixed with @user)
    message.reply('Yes, I can!')

    # Message is sent on the channel
    # message.send('I can help everybody!')'''

