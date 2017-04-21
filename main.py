#!/usr/bin/env python
# coding: utf-8

import gevent.monkey
gevent.monkey.patch_all()

import yaml
import logging
logging.basicConfig(level=logging.INFO)
import slackbot.settings
slackbot.settings.PLUGINS = [
    'slackbot_wechat_plugin',
]
slackbot.settings.API_TOKEN = yaml.load(file('config.yaml').read())['slack_token']
from slackbot.bot import Bot as SlackBot


def wxbot_main():
    from wxbot_slack import wxbot
    wxbot.DEBUG = True
    wxbot.conf['qr'] = 'tty'
    wxbot.is_big_contact = True   #如果确定通讯录过大，无法获取，可以直接配置，跳过检查。假如不是过大的话，这个方法可能无法获取所有的联系人
    wxbot.run()


def slackbot_main():
    slackbot = SlackBot()
    slackbot.run()

if __name__ == '__main__':
    gevent.joinall([gevent.spawn(wxbot_main), gevent.spawn(slackbot_main), ])
