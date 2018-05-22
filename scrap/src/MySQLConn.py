# -*- coding:utf-8 -*-
import MySQLdb


# 获取数据库链接
class MySqlConn(object):

    def __init__(self, address="vry360.com",
                 port="30308", username="root", password="vry360Testo1", database="hotel_product", coding="utf8"):
        self.address = address

        self.username = username

        self.password = password

        self.port = port

        self.coding = coding

        self.database = database

    def getconn(self):
        db = MySQLdb.connect(self.address+self.port, self.username, self.password, self.database, charset='utf8')
        return db


def get_default_sql(database_name="hotel_product"):
    # 链接数据库
    conn = MySQLdb.connect(host="vry360.com", port=30308, user="root", passwd="vry360Testo1", db=database_name,
                           charset="utf8", cursorclass=MySQLdb . cursors . DictCursor)
    return conn
