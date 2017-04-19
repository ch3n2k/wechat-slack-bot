#!/usr/bin/env python
# coding: utf-8

import gevent.monkey
gevent.monkey.patch_all()

from slackbot.bot import Bot as SlackBot

from wxbot_slack import wxbot

def wxbot_main():
    wxbot.DEBUG = True
    wxbot.conf['qr'] = 'tty'
    wxbot.is_big_contact = True   #如果确定通讯录过大，无法获取，可以直接配置，跳过检查。假如不是过大的话，这个方法可能无法获取所有的联系人
    wxbot.run()

def slackbot_main():
    slackbot = SlackBot()
    slackbot.run()

if __name__ == '__main__':
    gevent.joinall([gevent.spawn(wxbot_main), gevent.spawn(slackbot_main), ])
#    slackbot_main()
    #wxbot_main()
