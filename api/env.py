#!/usr/bin/python3
# coding:utf-8
"""
@File:   env.py
@Date:   2023/3/30 18:12
@Author: Alfred

"""
import os

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
SALT = os.environ.get('SALT')
VERCEL_URL = os.environ.get('VERCEL_URL')
PARSE_MODE = os.environ.get('PARSE_MODE')
if not PARSE_MODE:
    PARSE_MODE = 'MarkdownV2'
