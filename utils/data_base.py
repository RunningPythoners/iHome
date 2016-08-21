#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
import logging
from utils.common import get_master_db_conn
from utils.common import get_slaver_db_conn


class DataBase(object):

    def __init__(self):
        self._logging = logging.getLogger(self.__class__.__name__)
        self._db_master = get_master_db_conn()
        self._db_slaver = get_slaver_db_conn()

    def query(self, sql, **param):
        rows = []
        try:
            rows = self._db_slaver.query(sql, **param)
        except Exception as ex:
            self._logging.error("query error sql:%s, param:%s, msg:%s" % (sql, param, ex))
        finally:
            return rows

    def query_one(self, sql, **param):
        rows = None
        try:
            rows = self._db_slaver.query(sql, **param)
        except Exception as ex:
            self._logging.error("query error sql:%s, param:%s, msg:%s" % (sql, param, ex))
        finally:
            return rows[0] if rows else None

    def execute(self, sql, **param):
        result = -1
        try:
            self._db_master.begin()
            result = self._db_master.execute(sql, param)
            self._db_master.commit()
        except Exception as ex:
            self._db_master.rollback()
            self._logging.error("execute error sql:%s, param:%s, msg:%s" % (sql, param, ex))
        finally:
            return result

    def execute2(self, sql, **param):
        result = -1
        try:
            result = self._db_master.execute(sql, param)
        except Exception as ex:
            self._logging.error("execute error sql:%s, param:%s, msg:%s" % (sql, param, ex))
        finally:
            return result
