#!/usr/bin/python3
# coding:utf-8
"""
@File:   utils.py
@Date:   2023/3/30 17:34
@Author: Alfred

"""
from api.env import *
import requests


def set_webhook():
    set_webhook_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook'
    data = {
        'url': f'https://{VERCEL_URL}/api'
    }
    requests.post(set_webhook_url, data=data)


def send_message(chai_id, text, message_id=None):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': chai_id,
        'text': text,
        'parse_mode': PARSE_MODE
    }
    if message_id:
        data['reply_to_message_id'] = message_id
    requests.post(url, data=data)


# telegram MarkdownV2 字体样式
class Font:

    def bold(self, text):
        return f'*{text}*'

    def italic(self, text):
        return f'_{text}_'

    def underline(self, text):
        return f'__{text}__'

    def strikethrough(self, text):
        return f'~{text}~'

    def code(self, text):
        return f'`{text}`'

    def link(self, text, url):
        return f'[{text}]({url})'

    def hashtag(self, text):
        return f'#{text}'


font = Font()
