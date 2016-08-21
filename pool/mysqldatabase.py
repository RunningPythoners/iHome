# -*- coding: utf-8 -*- 
# 文件名: database.py
# 摘  要: MySQLdb封装

import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class MysqlAccount(object):
    """
    mysql account
    """

    def __init__(self, host, user, passwd, dbase, sock="", port=3306):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbase = dbase
        self.sock = sock
        self.port = int(port)


class DBConnection(object):
    """
    MySQLdb的简单封装
    """

    def __init__(self, dba):
        self.__dba = dba  # MysqlAccount
        self.__conn = ""
        self.__cursor = ""
        self.__err = ""
        self.__curdbase = ""
        self.connect(dba)

    def __del__(self):
        try:
            self.__conn.close()
        except:
            pass

    def connect(self, dba):
        """
        connect to mysql server
        """
        self.__dba = dba
        self.__conn = MySQLdb.connect(host=str(dba.host), user=str(dba.user), passwd=str(dba.passwd),
                                      db=str(dba.dbase), port=dba.port, charset="utf8")
        self.__cursor = self.__conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.execute("set names 'utf8'")
        self.__curdbase = dba.dbase
        return True

    def close(self):
        self.__conn.close()

    def auto_reconnect(self):
        """
        ping mysql server
        """
        try:
            self.__conn.ping()
        except Exception:
            self.__cursor.close()
            self.__conn.close()
            self.__cursor = None
            self.__conn = None
            self.connect(self.__dba)
        return True

    def execute(self, sql, args=None):
        lastrowid = -1
        if self.__cursor:
            self.auto_reconnect()
            self.__cursor.execute(sql, args)
            lastrowid = self.__cursor.lastrowid
        else:
            self.connect(self.__dba)
        return lastrowid

    def execute_many(self, sql, args=None):
        if self.__cursor:
            self.auto_reconnect()
            self.__cursor.executemany(sql, args)
        else:
            self.connect(self.__dba)

    def use_dbase(self, dbase):
        if self.__curdbase != dbase:
            sql = "use %s" % (dbase,)
            self.execute(sql)
            self.__curdbase = dbase
        return True

    def begin(self):
        try:
            self.__conn.begin()
        except Exception:
            self.__cursor.close()
            self.__conn.close()
            self.__cursor = None
            self.__conn = None
            self.connect(self.__dba)
            self.__conn.begin()


    def commit(self):
        self.__conn.commit()

    def rollback(self):
        self.__conn.rollback()

    def error(self):
        return self.__err

    def rows(self):
        return self.__cursor.fetchall()

    def row(self):
        return self.__cursor.fetchone()

    def connection(self):
        return self.__conn
