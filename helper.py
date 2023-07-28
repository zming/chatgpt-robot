# -*- coding: UTF-8 -*-

import hmac
import base64
import hashlib
import urllib.parse

from conf.config import CONF


def get_sign(timestamp):
    """ 消息数字签名计算核对
    :param timestamp:
    :param timestamp:
    :return:
    """
    app_secret = CONF.APPSECRET
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(str(timestamp), app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign


def check_sign(timestamp, sign):
    """
    :param timestamp:
    :param sign:
    :return:
    """
    return get_sign(timestamp) == sign
