import yaml
import db
import json

config = yaml.load(open('config.yaml').read())

slack_token = config['slack_token']

auto_accept = bool(config['auto_accept']) if 'auto_accept' in config else False

botadmin = config['botadmin'] if 'botadmin' in config else None

if botadmin and not botadmin.startswith("@"):
    botadmin = '@' + botadmin

wechat_slack_map = db.get_wechat_mappings()

slack_wechat_map = db.get_slack_mappings()

emoji_map = {i['short_name']: i['unified'] for i in json.load(open('emoji_pretty.json'))}


def set_mapping(group_name, channel_name):
    del_mapping(group_name, channel_name)
    db.set_mapping(group_name, channel_name)
    wechat_slack_map[group_name] = channel_name
    slack_wechat_map[channel_name] = group_name


def del_mapping(group_name, channel_name):
    db.del_mapping(group_name, channel_name)
    old_channel_name = wechat_slack_map[group_name] if group_name in wechat_slack_map else None
    old_group_name = slack_wechat_map[channel_name] if channel_name in slack_wechat_map else None
    if old_channel_name and old_channel_name in slack_wechat_map:
        del slack_wechat_map[old_channel_name]
    if old_group_name and old_group_name in wechat_slack_map:
        del wechat_slack_map[old_group_name]
    if group_name in wechat_slack_map:
        del wechat_slack_map[group_name]
    if channel_name in slack_wechat_map:
        del slack_wechat_map[channel_name]
