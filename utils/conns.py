# -*- coding: UTF-8 -*-
import json

import redis
import six


class RedisClient(object):
    """ 同步的Redis客户端
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str = '127.0.0.1', port: int = 6379, db: int = 0,
                password: str = None, decode_responses: bool = True, **kwargs):
        """
        :param host:
        :param port:
        :param db:
        :param password:
        :param decode_responses:
        :param args:
        :param kwargs:
        """
        connection_kwargs = {
            'host': host,
            'port': port,
            'db': db,
            'decode_responses': decode_responses
        }

        if password:
            connection_kwargs.update({'password': password})

        pool = redis.ConnectionPool(**connection_kwargs)
        self._client = redis.Redis(connection_pool=pool)

    def set(self, key, data, expire=None, *args, **kwargs):
        """
            :param key:
            :param data: 需要缓存的数据
            :param expire:
            :return:
            """
        if isinstance(data, (dict, list, tuple)):
            data = json.dumps(data)
        assert isinstance(data, six.string_types), 'cache_data foramt error, require dict'
        self._client.set(key, data)
        if expire:
            self._client.expire(key, expire)

    def get(self, key: str, *args, **kwargs) -> dict:
        """
        :param key: 缓存KEY
        :return:
        """

        data = self._client.get(key)
        if data:
            data = json.loads(data)
        else:
            data = {}

        if kwargs.get('pop', False):
            self._client.delete(key)

        return data

redis_cli = RedisClient()
