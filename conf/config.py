# -*- coding: UTF-8 -*-
import os


class Config(object):
    """
    """
    # 开发设置
    DEBUG = True
    AUTO_RELOAD = True
    CHECK_SIGN = True
    PORT = os.environ.get('PORT', 7070)
    LOG_FILE = 'logs/server.log'
    LOG_REMAIN = 30
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # 钉钉设置
    APPKEY = os.environ.get('APPKEY', '')
    APPSECRET = os.environ.get('APPSECRET', '')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

    # 使用设置
    QALOG = os.environ.get('QALOG', False)  # 是否开启记录


CONF = Config()
