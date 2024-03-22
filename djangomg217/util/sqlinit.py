# coding:utf-8
from configparser import ConfigParser
import logging, sys, os
import pymysql

from util.configread import config_read


class Create(object):
    def __init__(self, dbtype, host, port, user, passwd, dbName, charset):
        self.dbtype, self.host, self.port, self.user, self.passwd, self.dbName, self.charset = dbtype, host, port, user, passwd, dbName, charset
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port,
                                    charset=self.charset)
        self.cur = self.conn.cursor()

    def create_db(self, sql):
        self.cur.execute(sql)
        self.conn.commit()

    def create_tables(self, sqls):
        use_sql = '''use `{}`;'''.format(self.dbName)
        self.cur.execute(use_sql)

        for sql in sqls:
            self.cur.execute(sql)
            self.conn.commit()

    def conn_close(self):
        self.cur.close()
        self.conn.close()
