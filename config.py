import yaml
import db

config = yaml.load(open('config.yaml').read())

slack_token = config['slack_token']

wechat_slack_map = db.get_wechat_mappings()

slack_wechat_map = db.get_slack_mappings()

def set_mapping(group_name, channel_name):
    db.set_mapping(group_name, channel_name)
    wechat_slack_map[group_name] = channel_name
    slack_wechat_map[channel_name] = group_name


def del_mapping(group_name, channel_name):
    db.del_mapping(group_name, channel_name)
    del wechat_slack_map[group_name]
    del slack_wechat_map[channel_name]
