# -*- coding:utf-8 -*-
import MySQLConn


class CtripHotel(object):

    def __init__(self, ctrip_id, hotel_name, hotel_address, hotel_landmark, hotel_score, hotel_judgement_score, hotel_judgement):
        # 携程ID
        self.ctrip_id = ctrip_id

        # 酒店名称
        self.hotel_name = hotel_name

        # 酒店地址
        self.hotel_address = hotel_address

        self.hotel_landmark = hotel_landmark

        self.hotel_score = hotel_score

        self.hotel_judgement_score = hotel_judgement_score

        self.hotel_judgement = hotel_judgement


def insert(hotel_list_array):
    # 链接数据库
    conn = MySQLConn.get_default_sql("")

    # 通过cursor创建游标
    cursor = conn.cursor()

    # 拼接为字符串
    for item in hotel_list_array:
        try:
            # 创建sql 语句，并执行
            sql = 'insert into ctrip_hotel (`ctrip_id`,`hotel_name`,`hotel_address`,`hotel_landmark`,`hotel_score`,`hotel_judgement_score`,`hotel_judgement`) ' \
                  'values(%d, "%s","%s", "%s", "%s", "%s",%d)' % \
                  (item.ctrip_id, item.hotel_name, item.hotel_address, item.hotel_landmark,
                   item.hotel_score, item.hotel_judgement_score, item.hotel_judgement)
            cursor.execute(sql)
            # 提交SQL
            conn.commit()
        except Exception as e:
            # 重复记录
            print "Ctrip_id " + str(item.ctrip_id) +" already exist"
            continue
    # 关闭链接
    conn.close()
