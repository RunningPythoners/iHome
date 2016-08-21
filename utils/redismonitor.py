#!/usr/bin/python
# -*- coding: utf-8 -*- 
#
import time
import logging
import threading
from threading import Thread
from pool.redispool import RedisPool
from conf.jsonconst import REDIS_EVENT_CH_SUB_PATTERN

class _RedisMonitor(Thread):
    
    REDIS_MONITOR_THREAD_NAME = "RedisMonitor"

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        threading.Thread.__init__(self, name=self.REDIS_MONITOR_THREAD_NAME)
        self._logger = logging.getLogger(self.__class__.__name__)

    def initialize(self):
        self._stop = False
        
    def stop(self):
        self._stop = True
        
    def _listen(self, listener):
        while not self._stop:
            msg = listener.next()
            msgType = msg['type']
            channel = msg['channel']
            data = msg['data']
            self._logger.info("Receive redis event: type[%s], channel[%s], data[%s]", msgType, channel, data)
            try:
                pass
            except Exception as ex:
                self._logger.error("Handle message type[%s], channel[%s], data[%s], occured exception: %s", msgType, channel, data, str(ex))                

    def run(self):
        self._logger.info("Redis monitor start to work...")
        while not self._stop:
            try:
                redisConn = RedisPool.get_event_redis()
                pubsub = redisConn.pubsub()
                pubsub.psubscribe(REDIS_EVENT_CH_SUB_PATTERN)
                listener = pubsub.listen()
                self._listen(listener)
            except Exception as ex:
                self._logger.error("Occur exception:%s, when subscribe redis channel", str(ex), exc_info=1)
            finally:
                time.sleep(60 * 1)# sleep 1 minutes
                
RedisMonitor = _RedisMonitor.instance()
