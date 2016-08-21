#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
import torndb
import logging
from config import MYSQL_CONFIG_MASTER, MYSQL_CONFIG_SLAVER
from utils.rpc import RPC
from pool.mysqldatabase import MysqlAccount, DBConnection

        
class _DBConnPool(object):
    
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
            cls.__logger = logging.getLogger("dbconn_pool")
        return cls._instance

    def __init__(self):
        self._master_conf = MysqlAccount(host=MYSQL_CONFIG_MASTER["server"],
                                         user=MYSQL_CONFIG_MASTER["username"],
                                         passwd=MYSQL_CONFIG_MASTER["password"],
                                         dbase=MYSQL_CONFIG_MASTER["dbname"])
        # self._slaver_conf = []
        # for server in MYSQL_CONFIG_SLAVER:
        #     self._slaver_conf.append(
        #         MysqlAccount(host=server["server"],
        #                      user=server["username"],
        #                      passwd=server["password"],
        #                      dbase=server["dbname"])
        #     )

            
    def createMasterDataBaseConn(self):
        # db = torndb.Connection(
        #         MYSQL_CONFIG_MASTER["server"],
        #         MYSQL_CONFIG_MASTER["dbname"],
        #         user=MYSQL_CONFIG_MASTER["username"],
        #         password=MYSQL_CONFIG_MASTER["password"],
        #         time_zone="+8:00")
        db = DBConnection(self._master_conf)
        return db

    def createSlaverDataBaseConn(self):
        server = RPC.random_server(MYSQL_CONFIG_SLAVER)
        db = torndb.Connection(server["server"],
                server["dbname"],
                user=server["username"],
                password=server["password"],
                time_zone="+8:00")
        # server = RPC.random_server(self._slaver_conf)
        # db = DBConnection(server)
        return db
        
DBConnPool = _DBConnPool.instance()            
