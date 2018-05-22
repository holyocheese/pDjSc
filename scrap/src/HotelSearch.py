# -*- coding:utf-8 -*-


# 携程酒店列表请求类
class HotelSearch(object):

    def __init__(self, starttime, deptime, cityname, cityid, cityCode):

        self.startTime = starttime

        self.depTime = deptime

        self.cityName = cityname

        self.roomGuestCount = '1.1.0'

        self.isOnlyAirHotel = 'F'

        self.cityId = cityid

        self.cityCode = cityCode

    @staticmethod
    def getdefault(self):
        return HotelSearch("2018-05-29", "2018-05-30", "广州", "32", "020")

    # def insert(self):
    #     conn = mysqlconn()
    #     db = conn.getconn()

