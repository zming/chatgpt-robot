# -*- coding: UTF-8 -*-
import asyncio
import os
import openai
from utils.conns import redis_cli

OPENAI_KEY = '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'

openai.api_key = os.getenv("OPENAI_API_KEY", OPENAI_KEY)


# model = openai.Model.list()

async def chat_completion(message, model='gpt-3.5-turbo'):
    """
    :param message:
    :param model:
    :return:
    """
    messages = []
    current_message = {"role": "user", "content": message}
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": message}
        ]
    )
    if isinstance(completion, asyncio.Future):
        completion = await completion
    print("completion",type(completion))
    return completion


# completion = chat_completion('你好')
# print(completion.choices[0].message['content'])
