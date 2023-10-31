#!/usr/bin/python3
# coding:utf-8
"""
@File:   index.py
@Date:   2023/3/30 17:34
@Author: Alfred

"""
import hashlib
import traceback

import requests
from flask import Flask, request

from api.env import *
from api.utils import send_message, set_webhook, set_bot_commands, json_p


def create_app():
    set_webhook()
    set_bot_commands()

    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'Hello, World!'

    # @app.route('/env')
    # def env():
    #     return json.dumps(dict(os.environ), ensure_ascii=False, indent=4)

    @app.route('/send', methods=['GET', 'POST'])
    def send():
        if request.method == 'GET':
            # 获取sendkey  title  desc
            sendkey = request.args.get('sendkey')
            text = request.args.get('text')
        elif request.method == 'POST':
            # 判断请求体是否是json
            if not request.is_json:
                return '请求体不是json'
            # 获取sendkey  title  desc
            sendkey = request.json.get('sendkey')
            text = request.json.get('text')
        else:
            return 'not support. '
        # 检查sendkey
        if not sendkey or 'T' not in sendkey:
            return 'sendkey is invalid.'
        if not text:
            return 'text不能为空'
        # 获取用户id
        send_user, user_key = sendkey.split('T', 1)
        # 检查sendkey
        if user_key != hashlib.md5((send_user + SALT).encode('utf-8')).hexdigest():
            return 'sendkey不正确'
        # 发送消息
        return send_message(send_user, text)

    # receive message from telegram

    @app.route('/api', methods=['POST'])
    def api():
        ret = {'code': 0, 'msg': 'ok'}
        try:
            print(request.json)
            message = request.json
            # msg content
            text = message.get('message').get('text')
            # msg sender id
            chat_id = message.get('message').get('from').get('id')
            # msg id
            message_id = message.get('message').get('message_id')

            if text == '/start':
                msg = 'This is a telegram message bot. \n' \
                      'You can use /sendkey to get your sendkey. \n'
                send_message(chat_id, msg, message_id)
            elif text == '/sendkey':
                chat_id = str(chat_id)
                sendkey = chat_id + SALT
                sendkey = hashlib.md5(sendkey.encode('utf-8')).hexdigest()
                sendkey = f'{chat_id}T{sendkey}'
                send_message(int(chat_id), f'Use the url to send message: '
                                           f'{SEND_MSG_URL}?sendkey={sendkey}&text=<text>', message_id)
            else:
                ret['msg'] = 'not support.'
        except:
            print(traceback.format_exc())
            ret['code'] = 1
        json_p(ret)
        return ret
    # 以bot开头的url，正则

    @app.route('/bot<path:bot_api>', methods=['POST', 'GET'])
    def bot(bot_api):
        try:
            # 将请求转发给telegram api，get和post
            print(dict(request.headers).get('Content-Type', ''))
            if request.method == 'POST':
                if 'x-www-form-urlencoded' in dict(request.headers).get('Content-Type', ''):
                    return requests.post(TELEGRAM_API_URL + request.full_path, json=dict(request.form)).json()
                elif 'json' in dict(request.headers).get('Content-Type', ''):
                    return requests.post(TELEGRAM_API_URL + request.full_path, json=request.json).json()
                else:
                    return {'code': 2, 'msg': 'error'}
            elif request.method == 'GET':
                return requests.get(TELEGRAM_API_URL + request.full_path).json()
            else:
                return {'code': 3, 'msg': 'error'}
        except:
            print(traceback.format_exc())
            return {'code': 1, 'msg': 'error'}

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
