# -*- coding:utf-8 -*-


# 数据库基础类
class SqlBase(object):

    def __init__(self, id, insert_uid, insert_date, update_uid, update_date):

        self.id = id

        self.insert_uid = insert_uid

        self.insert_date = insert_date

        self.update_uid = update_uid

        self.update_date = update_date

