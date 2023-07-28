# -*- coding: UTF-8 -*-
import logging
import requests


logger = logging.getLogger(__name__)

def split_message_gracefully(message, max_length=5000):
    """ 优雅分割消息
    :param message:
    :param max_length:
    :return:
    """
    message_segments = []
    current_segment = ""

    separator = '.'
    if "。" in message:
        separator = '。'

    # 根据内容和长度进行分段
    for sentence in message.split(separator):
        sentence = sentence.strip()
        if len(current_segment + sentence) <= max_length:
            current_segment += sentence + separator
        else:
            message_segments.append(current_segment)
            current_segment = sentence + separator

    # 添加最后一个分段
    if current_segment:
        message_segments.append(current_segment)

    return message_segments

class DingTalkService(object):
    """ 钉钉消息发送服务
    """
    webhook_url = ''

    def post_data(self, data):
        """
        :param data:
        :return:
        """
        resp = requests.post(self.webhook_url, json=data)
        if not resp.ok:
            logger.error("发送钉钉报文错误 webhook=[{}], data=[{}]\n{}".format(self.webhook_url,
                                                                       data, resp.text))


    def send_text_message(self, message):
        """
        :param message:
        :return:
        """
        data = {
            "msgtype": "text",
            "text": {"content": message}
        }

        # 长度超过5000的消息，需要分段发送
        if len(message) > 5000:
            message_segments = split_message_gracefully(message)
            for message_segment in message_segments:
                data['text']['content'] = message_segment
                self.post_data(data=data)
            return

        self.post_data(data=data)

    def send_markdown_message(self, message, title, user_id):
        """
        :param message:
        :param user_id:
        :return:
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": message
            },
            "at": {
                "atUserIds": [
                    user_id
                ]
            }
        }
        self.post_data(data=data)

dingtalk_service = DingTalkService()