# -*- coding:utf-8 -*-
import MySQLConn

# 携程酒店列表请求类
class CtripCity(object):

    def __init__(self, ctrip_city_code, city_name, first_character, city_code=None, hotel_total_count=0, is_search=0):

        self.ctrip_city_code = ctrip_city_code

        self.is_search = is_search

        self.city_name = city_name

        self.hotel_total_count = hotel_total_count

        self.first_character = first_character

        self.city_code = city_code


def insert(data_list):
    # 链接数据库
    conn = MySQLConn.get_default_sql("hotel_product")

    # 通过cursor创建游标
    cursor = conn.cursor()

    # 循环写入数据库
    for item in data_list:
        try:
            # 创建sql 语句，并执行
            sql = 'insert into ctrip_city (`ctrip_city_code`,`is_search`,`city_name`,`hotel_total_count`,`first_character`,`city_code`) ' \
                  'values("%s", %d,"%s", %d, "%s", "%s")' % \
                  (item.ctrip_city_code, item.is_search, item.city_name, item.hotel_total_count,
                   item.first_character, item.city_code)
            cursor.execute(sql)
            # 提交SQL
            conn.commit()
        except Exception as e:
            # 重复记录
            print e
            print "ctrip_city_code " + str(item.ctrip_city_code) +" already exist"
            continue
    # 关闭链接
    conn.close()
