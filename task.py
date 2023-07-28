# -*- coding: UTF-8 -*-
import os
from datetime import datetime
from service import chat_completion, dingtalk_service
from utils.conns import redis_cli
from sanic.log import logger
from conf.config import CONF

def process_message(question, message_id):
    """
    :param question:
    :param message_id:
    :return:
    """
    req_data = redis_cli.get(message_id)
    if not req_data:
        logger.error("消息ID[{}]没有找到缓存数据".format(message_id))
        return

    conversation_id = req_data['conversationId']
    answer = chat_completion(message=question,
                             conversation_id=conversation_id)
    # print("answer", answer)

    if CONF.QALOG:
        sender_staff_id = req_data['senderStaffId']
        log_file_dir = os.path.join(os.path.dirname(__name__), 'logs')
        if not os.path.exists(log_file_dir):
            os.makedirs(log_file_dir)
        log_file = os.path.join(log_file_dir, '{}.log'.format(sender_staff_id))

        create_at = datetime.fromtimestamp(req_data['createAt'] / 1000)
        question_record = '{} {}[{}] 提问: {}\n'.format(create_at.isoformat(),
                                               req_data['senderNick'],
                                                sender_staff_id,
                                               question)
        answer_record = '{} chatGPT[{}] 回答: {}\n'.format(datetime.now().isoformat(),
                                                    CONF.OPENAI_MODEL,
                                                    answer)

        with open(log_file,'a') as fp:
            fp.write(question_record)
            fp.write(answer_record)


    dingtalk_service.webhook_url = req_data['sessionWebhook']
    dingtalk_service.send_text_message(message=answer)

    # sender_staff_id = 'manager7045'
    # dingtalk_service.send_markdown_message(message=answer,title='Test',
    #                                        user_id=sender_staff_id)