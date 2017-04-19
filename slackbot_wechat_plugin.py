from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re

import slackbot.bot as bot
from slackbot.dispatcher import Message
from slackbot.slackclient import Channel

from wxbot_slack import wxbot

config=yaml.load(file('config.yaml').read())
slack_wechat_map = dict((x, w) for w, x in config['bindings'].iteritems())

@listen_to('.*')
def any_message(message):
    print message.body
    if message.body['type'] == 'message':
        channel_name = message.channel._client.channels[message.body['channel']]['name']
        username = message.channel._client.users[message.body['user']]['name']
        print channel_name, username
        if channel_name in slack_wechat_map:
            group_name = slack_wechat_map[channel_name]
            wxbot.send_msg(group_name, username + ' said: ' + message.body['text'])
    else:
        print 'unable to process the message'

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

