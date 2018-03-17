import slackbot.settings
from . import config
slackbot.settings.PLUGINS = [
    'wxslack.slackbot_wechat_plugin',
]
slackbot.settings.ERRORS_TO = 'wechat-bot-support'
slackbot.settings.API_TOKEN = config.slack_token
from slackbot.bot import Bot as SlackBot

slackbot = SlackBot()

def slackbot_main():
    slackbot.run()
