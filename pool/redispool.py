#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import logging
import redis
from redis_shard.shard import RedisShardAPI
from config import REDIS_CONFIG_EVENT, REDIS_CONFIG_STAT, REDIS_CONFIG_CACHE


class _RedisPool(object):

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
            cls._logger = logging.getLogger("redis_pool")
        return cls._instance
    
    def __init__(self):
        pass
        
    def initialize(self):
        self._redis_stat_pool = redis.ConnectionPool(host=REDIS_CONFIG_STAT['server'], port=REDIS_CONFIG_STAT['port'], db=REDIS_CONFIG_STAT['db'])
        self._redis_event_pool = redis.ConnectionPool(host=REDIS_CONFIG_EVENT['server'], port=REDIS_CONFIG_EVENT['port'], db=REDIS_CONFIG_EVENT['db'])
        self._logger.info("Redis connection pool initialize success.")

    def get_cache_redis(self):
        return RedisShardAPI(REDIS_CONFIG_CACHE)

    def get_stat_redis(self):
        return redis.Redis(connection_pool=self._redis_stat_pool)

    def free_stat_redis(self, redisConn):
        self._redis_stat_pool.release(redisConn)

    def get_event_redis(self):
        return redis.Redis(connection_pool=self._redis_event_pool)
    
    def free_event_redis(self, redisConn):
        self._redis_event_pool.release(redisConn)

    def close(self):
        if self._redis_event_pool:
            self._redis_event_pool.disconnect()
            self._redis_enevt_pool = None
        if self._redis_stat_pool:
            self._redis_stat_pool.disconnect()
            self._redis_stat_pool = None

RedisPool = _RedisPool.instance()
