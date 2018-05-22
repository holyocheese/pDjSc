#-*- coding:utf-8 -*-
import requests


if __name__ == "__main__":
    param = {"StartTime": "2018-05-18", "DepTime": "2018-05-19", "cityName": "广州","RoomGuestCount": "1,1,0",
             "IsOnlyAirHotel": "F","cityId": 32,"cityCode": 020}
    list = "http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx"
    html = requests.post(list,data=param)
    print html.text