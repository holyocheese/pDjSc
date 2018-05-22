#-*- coding:utf-8 -*-
import os
import sys
from time import ctime
from time import sleep
import HotelSearch as hs
import requests
from bs4 import BeautifulSoup as Bs
import CtripHotel as ch
import CtripCity as cc
import MySQLdb
import MySQLConn

sys.path.append("..")
reload(sys)
sys.setdefaultencoding('utf-8')
# 统一访问session
print os.path
# 连接数
requests.adapters.DEFAULT_RETRIES = 10
se = requests.session()
se.keep_alive = False
# 代理服务器
# se.proxies = {"https://"}


class Ctrip(object):

    def __init__(self, citycode, scraptype=0):
        # 爬取类型
        self.scrap_type = scraptype
        # 酒店Index
        self.index = "http://hotels.ctrip.com"
        # 酒店详情页
        self.mainUrl = "http://hotels.ctrip.com/hotel/"
        # 列表请求
        self.list = "http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx"
        # 城市代码
        self.citycode = citycode
        # 酒店搜索类
        self.hs = hs
        # 请求头
        self.header = {"Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
                        "Cache-Control": "max-age=0",
                        "Connection": "keep-alive",
                        "Content-Length": "1800",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                               "Referer":"http://hotels.ctrip.com/hotel/guangzhou32",
                                               "Host":"hotels.ctrip.com"}

        self.citylist = "http://hotels.ctrip.com/citylist"

    # 获取携程地区编码 并存入数据库
    def getcity(self):
        html = requests.get(self.citylist)
        bsObj = Bs(html.text, 'lxml')
        # 地址列表
        city_list = bsObj.findAll("div", {"class": "custom_list"})
        for city_item in city_list:
            # 首字母
            first_char = city_item.find("dt").text
            # 循环地区中文、编码
            code_list = city_item.findAll("dd")
            # 待插入列表
            data_list = []
            for code_item in code_list:
                # 城市名称
                city_name = code_item.find("a").text
                # 城市链接
                city_url = code_item.find("a").attrs['href']
                try:
                    # 城市编码
                    ctrip_city_code = city_url[city_url.find("l/")+2:]
                except Exception as e:
                    print e
                # 获取数据库链接
                try:
                    conn_base = MySQLConn.get_default_sql(database_name="hotel_base")
                    sql = 'SELECT city_code FROM city WHERE city_name = "%s" ' % city_name
                    # 通过cursor创建游标
                    cursor = conn_base.cursor()
                    cursor.execute(sql)
                    # 提交SQL
                    conn_base.commit()
                    # 获取所有记录列表
                    results = cursor.fetchall()
                    for x in results:
                        city_code = x[0]
                    print ctrip_city_code + city_name + first_char + city_code
                    city_sql = cc.CtripCity(ctrip_city_code, city_name, first_char, city_code=city_code)
                    data_list.append(city_sql)
                except Exception as e:
                    print e
            # 插入至数据库
            cc.insert(data_list)



    def getsearchHotelList(self, citycode):
        # 获取总页数
        totalpage = self.gettotalpage(self.citycode)
        unreadlist = []
        loop = range(1, (int(totalpage)+1))
        # 逐页查询
        for x in loop:
            try:
                # 打开第x页
                html = requests.get(self.mainUrl + str(citycode) + "/p" + str(x))
                print "page " + str(x) + " is Searching"
                bsObj = Bs(html.text, 'lxml')
                hotel_list = bsObj.find("div", {"id": "hotel_list"}).findAll("div", {"class": "hotel_new_list"})
                # 异步请求方式爬取
                # param = {"StartTime": "2018-05-22", "DepTime": "2018-06-19", "cityName": "广州",
                #          "RoomGuestCount": "1,1,0",
                #          "IsOnlyAirHotel": "F", "cityId": 32, "cityCode": 020, "page": x}
                # list = "http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx"
                # html = requests.post(list, data=param, headers=self.header)
                # bsObj = Bs(html.text.replace("\\", ""), 'lxml')
                # hotel_list = bsObj.findAll("div", {"class": "hotel_new_list"})
                # 数据转换
                hotel_total_list = self.bsobj_to_hotelobj(hotel_list)
                # 批量插入至数据库
                ch.insert(hotel_total_list)
            except Exception as e:
                print "Something goes wrong:"
                print e
                print "Wait a Minute,just sleep for a while"
                print "Zzzz"
                sleep(10)
                # 未读取列表
                unreadlist.append(x)
                print "Go on~"
                continue
        # 未查询成功的数据
        for i in unreadlist:
            try:
                # 打开第x页
                newse = requests.session()
                html = newse.get(self.mainUrl + str(self.citycode) + "/p" + str(i))
                print "page " + str(i) + " is Searching"
                bsObj = Bs(html.text, 'lxml')
                hotel_list = bsObj.find("div", {"id": "hotel_list"}).findAll("div", {"class": "hotel_new_list"})
                # 数据转换
                hotel_total_list = self.bsobj_to_hotelobj(hotel_list)
                # 批量插入至数据库
                self.insert(hotel_total_list)
            except Exception as e:
                print e
                continue

    # 转换至酒店列表
    def bsobj_to_hotelobj(self, bsobj):
        hotel_total_list = []
        # 循环酒店列表获取酒店信息
        for hotel_item in bsobj:
            # 酒店名称
            hotel_name = hotel_item.find("h2", {"class": "hotel_name"}).find("a").attrs['title']
            # 酒店ID
            ctripid = hotel_item.attrs["id"]
            # 酒店评分
            try:
                hotel_score = hotel_item.find("span", {"class": "hotel_value"}).text
            except:
                hotel_score = 0
            # 酒店地址
            try:
                hotel_address = hotel_item.find("p", {"class": "hotel_item_htladdress"}).text
                hindex = hotel_address.index("】")
                eindex = hotel_address.find("。")
                hotel_landmark = ""
                if hindex > 0 :
                    hotel_landmark = hotel_address[1:hindex]
                    if eindex >0:
                        hotel_address = hotel_address[hindex + 1:eindex]
                    else:
                        hotel_address = hotel_address[hindex + 1:]
                else:
                    hotel_address = ""
            except Exception as e:
                hotel_landmark = ""
                hotel_address = ""
            # 酒店起价
            # hotel_price = hotel_item.find("span", {"class": "J_price_lowList"}).text
            try:
                # 推荐百分比
                hotel_judgement_score = hotel_item.find("span", {"style": "color:#009933;"}).text
                # 点评人数
                hotel_judgement = hotel_item.find("span", {"style": "color:#FF9900;"}).text
            except Exception as e:
                hotel_judgement_score = 0
                hotel_judgement = 0
            # 等级
            # hotel_star = hotel_item.find("")
            # icon 列表
            # icon_list = hotel_item.find("div", {"class": "icon_list"}).findAll("i")
            hotel_obj = ch.CtripHotel(int(ctripid), hotel_name, hotel_address, hotel_landmark, hotel_score,
                                      hotel_judgement_score, int(hotel_judgement))
            hotel_total_list.append(hotel_obj)
        return hotel_total_list

    def insert(self, hotel_list_array):
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


if __name__ == "__main__":
    # 标记开始时间
    begintime = ctime()
    print "Scrap starts at " + ctime()
    # 初始化类
    ctrip = Ctrip(scraptype=1, citycode="guangzhou32")
    ctrip.getcity()
    print "Scrap ends at " + ctime()

