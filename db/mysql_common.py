# coding:utf-8
import MySQLdb


class MysqlCommon:
    __host = ''
    __port = 0
    __user = ''
    __pwd = ''
    __db = ''

    def __init__(self, host, port, user, pwd, db):
        self.__host = host
        self.__port = port
        self.__pwd = pwd
        self.__user = user
        self.__db = db

    def fetch_data(self, sql):
        conn = MySQLdb.connect(host=self.__host, port=self.__port, user=self.__user, passwd=self.__pwd, db=self.__db,
                               charset="utf8")
        cursor = conn.cursor()
        cursor.execute(sql)

        result = []
        for row in cursor.fetchall():
            result.append(row)

        return result

    def fetch_count(self, sql):
        conn = MySQLdb.connect(host=self.__host, port=self.__port, user=self.__user, passwd=self.__pwd, db=self.__db,
                               charset="utf8")
        cursor = conn.cursor()
        cursor.execute(sql)

        return cursor.fetchone()
