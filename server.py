# -*- coding: UTF-8 -*-
import os
import time

from sanic import Sanic
from conf import CONF, LOG_SETTINGS
from sanic.response import json, text
from redis import Redis
from rq import Queue
from task import process_message
from helper import check_sign
from utils.conns import redis_cli

# from service.chatgpt import chat_completion

# app = Sanic(__name__)

queue = Queue(connection=Redis())

def create_app(name, config: dict = None, log_config: dict = None):
    """
    :param name:  Sanic实例名称
    :param config: Sanic实例配置
    :return:
    """
    app = Sanic(name, log_config=log_config)
    app.config.update_config(config)
    return app


# 实例化 Sanic 类, 返回一个 sanic 应用
app = create_app(name=__name__, config=CONF, log_config=LOG_SETTINGS)

@app.route("/")
async def index(request):
    return text('ok')



@app.route("/message", methods=['GET', 'POST'])
async def message(request):
    """
    :param request:
    :return:
    """
    req_data = request.json

    '''
    {
	'conversationId': 'cidd6tSBCqaWTexLCY6As7/bYFhQr0bSGo2tI+GgANcgS4=',
	'chatbotCorpId': 'ding73a215893ab8c286a1320dcb25e91351',
	'chatbotUserId': '$:LWCP_v1:$YIyUfX+rtLu1UceiXVq+xdMT3PhXJv2m',
	'msgId': 'msg4nRTbhem8Di4bPhAjPUahA==',
	'senderNick': '覃志明',
	'isAdmin': True,
	'senderStaffId': 'manager7045',
	'sessionWebhookExpiredTime': 1689777797160,
	'createAt': 1689772395343,
	'senderCorpId': 'ding73a215893ab8c286a1320dcb25e91351',
	'conversationType': '1',
	'senderId': '$:LWCP_v1:$aN1hnLEpp2ZP40Gz9GhuPg==',
	'sessionWebhook': 'https://oapi.dingtalk.com/robot/sendBySession?session=ff09bb2f960eabb55dee62f9f7e802d9',
	'text': {
		'content': 'Hi'
	},
	'robotCode': 'ding7nr1tddq1hhq31x1',
	'msgtype': 'text'
    }
    '''





    headers = request.headers
    timestamp = headers.get("timestamp")
    sign = headers.get("sign")
    token = headers.get("token")

    # 校验请求是否合法
    if CONF.CHECK_SIGN and timestamp and sign:
        current_time = int(time.time())
        if abs(current_time - int(timestamp)/1000) > 60 * 60 * 1:
            return json({})

        if not check_sign(timestamp,sign):
            return json({})

    message_id = req_data['msgId']
    question = req_data['text']['content']
    # conversation_id = req_data['conversationId']
    # session_webhook = req_data['sessionWebhook']
    redis_cli.set(message_id, data=req_data, expire=5400)

    queue.enqueue(process_message, question, message_id)

    # answer = chat_completion(message=question, conversation_id=conversation_id)


    # queue.enqueue(time_sleep)

    # req_data['text']['content'] = answer

    return json({})

def run():
    workers = os.cpu_count()
    app.run(host="0.0.0.0",
            port=int(CONF.PORT),
            auto_reload=CONF.AUTO_RELOAD,
            workers=workers,
            )

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        import traceback
        traceback.print_exc()