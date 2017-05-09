#!/usr/bin/env python
# coding: utf-8

#import gevent.monkey
#gevent.monkey.patch_all()

import logging
logging.basicConfig(level=logging.INFO)

from wxbot_slack import wxbot
from wxpy import embed

def wxbot_main():
    embed()

from slackbot_main import slackbot_main

if __name__ == '__main__':
    slackbot_main()
    #wxbot_main()


