#!/usr/bin/python
# -*- coding: utf-8 -*- 
#
import time
import logging
import threading
import json
from threading import Thread
from pool.redispool import RedisPool
import Queue 
import importlib
from redis.exceptions import ConnectionError
from utils.common import get_stat_redis_conn
from conf.jsonconst import ASYNC_QUEUE_NAME 


class _AsyncRunRedisTask(Thread):
    
    THREAD_NAME = "AsyncRunRedisTask"

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        threading.Thread.__init__(self, name=self.THREAD_NAME)
        self._logger = logging.getLogger(self.__class__.__name__)

    def initialize(self):
        self._stop = False
        
    def deal(self, data):
        num = data.get("num", None)
        py = data.get("py", None)
        module = data.get("module", None)
        fun = data.get("fun", None)
        param = data.get("param", None)
        if not module or not fun or not py:
            return
        pym = importlib.import_module(py)
        m = getattr(pym, module)
        if m:
            f = getattr(m, fun)
            if f:
                if param:
                    f(**param)
                else:
                    f()

    def run(self):
        self._logger.info("async run start to work...")
        while not self._stop:
            try:
                redisConn = RedisPool.get_stat_redis()
                while True:
                    data = redisConn.brpop(ASYNC_QUEUE_NAME)
                    if not data:
                        continue
                    data = data[1]
                    self.deal(json.loads(data))
            except ConnectionError as ex:
                self._logger.error("Occur exception:%s", str(ex), exc_info=1)
                time.sleep(60 * 1)
            except Exception as ex:
                self._logger.error("Occur exception:%s", str(ex), exc_info=1)

    def add_task(self, data):
        get_stat_redis_conn().lpush(ASYNC_QUEUE_NAME, json.dumps(data))


class _AsyncRunLocalCacheTask(Thread):
    
    THREAD_NAME = "AsyncRunLocalCacheTask"

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def initialize(self):
        self._stop = False
        self._queue = Queue.Queue()

    def __init__(self):
        threading.Thread.__init__(self, name=self.THREAD_NAME)
        self._logger = logging.getLogger(self.__class__.__name__)

    def deal(self, data):
        callback = data.get("callback", None)
        if callback:
            callback()

    def run(self):
        self._logger.info("async run local cache start to work...")
        while not self._stop:
            try:
                while True:
                    data = self._queue.get()
                    if not data:
                        time.sleep(5)
                        continue
                    self.deal(data)
            except Exception as ex:
                self._logger.error("Occur exception:%s", str(ex), exc_info=1)
            finally:
                time.sleep(60 * 1)# sleep 1 minutes

    def add_task(self, data):
        self._queue.put(data)

AsyncRunRemoteCache = _AsyncRunRedisTask.instance()
AsyncRunLocalCache = _AsyncRunLocalCacheTask.instance()
