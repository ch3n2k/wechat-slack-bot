import yaml
import slackbot.settings
slackbot.settings.PLUGINS = [
    'slackbot_wechat_plugin',
]
slackbot.settings.ERRORS_TO = 'wechat-bot-support'
slackbot.settings.API_TOKEN = yaml.load(open('config.yaml').read())['slack_token']
from slackbot.bot import Bot as SlackBot

slackbot = SlackBot()

def slackbot_main():
    slackbot.run()