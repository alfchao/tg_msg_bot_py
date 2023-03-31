#!/usr/bin/python3
# coding:utf-8
"""
@File:   index.py
@Date:   2023/3/30 17:34
@Author: Alfred

"""
import hashlib
import traceback

from flask import Flask, request

from api.env import *
from api.utils import set_webhook, send_message


def create_app():
    set_webhook()
    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'Hello, World!'

    @app.route('/send', methods=['GET', 'POST'])
    def send():
        if request.method == 'GET':
            # 获取sendkey  title  desc
            sendkey = request.args.get('sendkey')
            text = request.args.get('text')
            # 检查sendkey
            if not sendkey:
                return 'sendkey不能为空'
            if not text:
                return 'title不能为空'
            # 获取用户id
            send_user, user_key = sendkey.split('T', 1)
            # 检查sendkey
            if user_key != hashlib.md5((send_user + SALT).encode('utf-8')).hexdigest():
                return 'sendkey不正确'
            # 发送消息
            send_message(send_user, text)
            return 'ok'
        elif request.method == 'POST':
            # 判断请求体是否是json
            if not request.is_json:
                return '请求体不是json'
            # 获取sendkey  title  desc
            sendkey = request.json.get('sendkey')
            text = request.json.get('text')

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
                msg = 'This is a telegram message bot\. \n' \
                      'You can use /sendkey to get your sendkey\. \n'
                send_message(chat_id, msg, message_id)
            elif text == '/sendkey':
                site_url = f'https://{VERCEL_URL}'
                chat_id = str(chat_id)
                sendkey = chat_id + SALT
                sendkey = hashlib.md5(sendkey.encode('utf-8')).hexdigest()
                sendkey = f'`{chat_id}T{sendkey}`'
                send_message(int(chat_id), f'Your sendkey 🔑 is {sendkey}\.\n'
                             f'Use the url to send message: \n'
                             f'{site_url}/api/send?sendkey=<sendkey>&text=<text>',  message_id)
            else:
                ret['msg'] = 'not support.'
        except:
            print(traceback.format_exc())
            ret['code'] = 1
        return ret

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
