# -*- coding: UTF-8 -*-
import requests
import os
import json
from sanic.log import logger
from utils.conns import redis_cli

OPENAI_KEY = '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'
OPENAI_KEY = os.getenv("OPENAI_API_KEY", OPENAI_KEY)

MODEL = "gpt-3.5-turbo-0301"

ROLE_USER = "user"
ROLE_SYSTEM = "system"
ROLE_ASSISTANT = "assistant"

messages = []

# 设置请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + OPENAI_KEY
}


def get_context(conversation_id, chat_type='dingtalk'):
    """ 获取上下文
    :return:
    """
    messages = []
    cache_key = 'CHAT:{}:{}'.format(chat_type, conversation_id)
    cache_data = redis_cli.get(cache_key)
    if cache_data:
        for item in cache_data:
            messages.append({
                'role': item['role'],
                'content': item['content']
            })
    return messages


def cache_context(conversation_id, context, chat_type='dingtalk', limit=6):
    """ 缓存上下文
    :return:
    """
    context = context or []

    cache_key = 'CHAT:{}:{}'.format(chat_type, conversation_id)

    redis_cli.set(cache_key, context[-limit:], expire=60 * 60 * 24 * 30)



def chat_completion(message, conversation_id:str=''):
    """
    :param message:
    :return:
    """
    messages = []

    # 获取上下文
    if conversation_id:
        context = get_context(conversation_id)
        messages.extend(context)

    # 当前消息
    current_message = {"role": "user", "content": message}
    messages.append(current_message)

    req_data = {
        "model": MODEL,
        "messages": messages
    }

    print("--------------ROUTER MSG [URL SETTING]--------------")
    print(messages)

    # 发送 HTTP POST 请求
    resp = requests.post(url='https://api.openai.com/v1/chat/completions',
                         headers=headers,
                         data=json.dumps(req_data))

    if not resp.ok:
        logger.error("请求OPNEAI API错误:{}".format(resp.text))
        return ''

    # print("resp", resp.text, flush=True)

    resp_data = resp.json()
    answer = resp_data["choices"][0]["message"]["content"].strip()

    print("--------------ROUTER MSG [CONVERSATION]--------------")
    print(resp_data["choices"])

    messages.append({"role": "assistant", "content": answer})

    cache_context(conversation_id, context=messages)

    return answer


def dealMsg(role, msg):
    """
    :param role: 角色【system,user,assistant】
    :param msg: 聊天信息
    """
    if len(messages) == 0:
        if msg == "":
            # system 默认角色
            msg = "你是一个聊天助手与我聊天，回答我，你是什么角色？"
        else:
            msg = "假设你是" + msg
    messages.append({"role": role, "content": msg})
    return messages
