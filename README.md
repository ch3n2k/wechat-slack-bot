
**wechat-slack-bot** 是基于[WxBot](https://github.com/liuwons/wxBot)和[slackbot](https://github.com/lins05/slackbot)的群聊消息同步机器人。

目前的支持情况:

- [ ] 群消息
  - [x] 文本
  - [x] 图片
  - [ ] 地理位置
  - [ ] 个人名片
  - [ ] 语音
  - [ ] 动画
  - [ ] 语音电话
  - [ ] 红包



## 使用指南

创建slack机器人，记下slack token。

创建slack channel。将slack机器人加入channel。

创建微信聊天群，群需要有一个固定的名字，并保存在通讯录。将机器人（某个微信帐号）加入微信群。

将 config.yaml.tmpl 改名为 config.yaml ，在该文件中添加slack token和群组映射关系。

安装python。安装依赖（ pip install -r requirements.txt ）。

运行 python main.py 启动应用，微信扫码登录。

