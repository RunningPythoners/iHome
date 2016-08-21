#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging.handlers
import os.path
import threading
from datetime import datetime, date
from pool.redispool import RedisPool
from pool.dbconnpool import DBConnPool


DATETIME = datetime.today().strftime("%Y%m%d")
FORMAT = '%(asctime)s - %(levelname)s: %(message)s'


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def set_logger(path, fmt_str=FORMAT, level=logging.DEBUG):
    _, filename = os.path.split(path)
    file_hdl = logging.handlers.TimedRotatingFileHandler(
        filename=path,
        when='D', interval=1, backupCount=30, encoding='utf-8')
    file_hdl.setFormatter(logging.Formatter(fmt_str))
    logger = logging.getLogger(filename.split('.')[0])
    logger.addHandler(file_hdl)
    logger.setLevel(level)
    return logger


def get_cache_redis_conn():
    localData = threading.currentThread().__dict__
    cacheRedis = localData.get('cache_redis', None)
    if cacheRedis is None:
        cacheRedis = RedisPool.get_cache_redis()
        localData['cache_redis'] = cacheRedis
    return cacheRedis


def get_stat_redis_conn():
    localData = threading.currentThread().__dict__
    statRedis = localData.get('stat_redis', None)
    if statRedis is None:
        statRedis = RedisPool.get_stat_redis()
        localData['stat_redis'] = statRedis
    return statRedis


def get_event_redis_conn():
    localData = threading.currentThread().__dict__
    eventRedis = localData.get('event_redis', None)
    if eventRedis is None:
        eventRedis = RedisPool.get_event_redis()
        localData['event_redis'] = eventRedis
    return eventRedis


def get_master_db_conn():
    localData = threading.currentThread().__dict__
    masterDB = localData.get('master_db', None)
    if masterDB is None:
        masterDB = DBConnPool.createMasterDataBaseConn()
        localData['master_db'] = masterDB
    return masterDB

def get_slaver_db_conn():
    localData = threading.currentThread().__dict__
    slaverDB = localData.get('slaver_db', None)
    if slaverDB is None:
        slaverDB = DBConnPool.createSlaverDataBaseConn()
        localData['slaver_db'] = slaverDB
    return slaverDB