#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#

import logging
import datetime
import Queue, threading
from threading import Thread
from pool.dbconnpool import DBConnPool
from pool.redispool import RedisPool
from conf.settings import THREAD_POOL_COUNT, WORKER_QUEUE_SIZE

class _Worker(Thread):
    '''
    worker thread which get task from queu to execute
    '''
    class _ProcessParam(object):
        
        def __init__(self, dbconn, eventRedisconn, statRedisConn, cacheRedisConn):
            self._dbconn = dbconn
            self._eventRedisconn = eventRedisconn
            self._statRedisConn = statRedisConn
            self._cacheRedisConn = cacheRedisConn

        @property
        def dbconntion(self):
            return self._dbconn

        @property
        def eventRedisConn(self):
            return self._eventRedisconn

        @property
        def statRedisConn(self):
            return self._statRedisConn
            
        @property
        def cacheRedisConn(self):
            return self._cacheRedisConn

    def __init__(self, threadname, workQueue, parent):
        threading.Thread.__init__(self, name=threadname)
        self.__logger = logging.getLogger(threadname)
        self.__parent = parent
        self.__workQueue = workQueue
        self.stop = False

    def run(self):
        while not self.stop:
            try:
                callback = self.__workQueue.get()
                if not callback:
                    continue
                     
                try:
                    callback()
                except Exception as processEx:
                    self.__logger.exception("%s execute callback: %r failed due to %s", self.name, callback, str(processEx))
            except IOError:
                pass
            except Exception as getEx:
                self.__logger.error("%s get task from queue failed: %s", self.name, getEx)
            
        
class _WorkerManager(object):
    
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
            cls.__logger = logging.getLogger("thread_pool")
        return cls._instance
        
    def initialize(self, workerCount=THREAD_POOL_COUNT):
        self.__workQueue = Queue.Queue(maxsize=WORKER_QUEUE_SIZE)
        self.__workerCount = workerCount
        self.__workers = []   
        for i in range(self.__workerCount):
            worker = _Worker("_Worker-" + str(i + 1), self.__workQueue, self)
            worker.start()
            self.__workers.append(worker)
            
    def add_task(self, callback):
        self.__workQueue.put(callback)
        
ThreadPool = _WorkerManager.instance()            
