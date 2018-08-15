# -*- coding: utf-8 -*-
import math

import requests

from geographiclib.geodesic import Geodesic


# get_distance 两个坐标的距离
def Distance(lon1, lat1, lon2, lat2):
    earth_padius = 6378.137  # 地球赤道半径（千米）,地球平均半径=6371.004 千米
    PI = 3.14159265358979324
    s = 0
    radlon1 = lon1 * PI / 180.0
    radlon2 = lon2 * PI / 180.0

    s = 2 * math.asin(
        math.sqrt(
            math.power(math.sin((radlon1 - radlon2) / 2), 2) +
            math.cos(radlon1) * math.cos(radlon2) *
            math.power(math.sin(((lat1 - lat2) * PI / 180.0) / 2), 2)))
    s = s * earth_padius
    return round(s * 1000, 2)  # 精确到米


def Azimuth(lonA, latA, lonB, latB):
    """
        Returns:
                bearing between the two GPS points,
                default: the basis of heading direction is north
        """
    radLatA = math.radians(latA)
    radLonA = math.radians(lonA)
    radLatB = math.radians(latB)
    radLonB = math.radians(lonB)
    dLon = radLonB - radLonA
    y = math.sin(dLon) * math.cos(radLatB)
    x = math.cos(radLatA) * math.sin(radLatB) - math.sin(radLatA) * math.cos(
        radLatB) * math.cos(dLon)
    brng = math.degrees(math.atan2(y, x))
    brng = (brng + 360) % 360
    return brng


def azimuthAngle(x1, y1, x2, y2):
    angle = 0.0
    dx = x2 - x1
    dy = y2 - y1
    if x2 == x1:
        angle = math.pi / 2.0
        if y2 == y1:
            angle = 0.0
        elif y2 < y1:
            angle = 3.0 * math.pi / 2.0
    elif x2 > x1 and y2 > y1:
        angle = math.atan(dx / dy)
    elif x2 > x1 and y2 < y1:
        angle = math.pi / 2 + math.atan(-dy / dx)
    elif x2 < x1 and y2 < y1:
        angle = math.pi + math.atan(dx / dy)
    elif x2 < x1 and y2 > y1:
        angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
    return (angle * 180 / math.pi)


def AmapGeocode(ak, address):
    """gaodeAPI:根据传入地名参数获取经纬度"""
    res = requests.get("http://restapi.amap.com/v3/geocode/geo",
                       params={'address': address, 'key': ak}).json()
    lng, lat = 0, 0
    if res["info"] == 'OK' and res["count"] != '0':
        lng, lat = res['geocodes'][0]['location'].split(',')
    return float(lng), float(lat)


def BdmapGeocode(ak, address):
    """baiduAPI:根据传入地名参数获取经纬度"""
    res = requests.get('http://api.map.baidu.com/geocoder/v2/',
                       params={'address': address, 'output': 'json', 'ak': ak}).json()
    lng, lat = 0, 0
    if res['status'] == 0:
        lng = res['result']['location']['lng']
        lat = res['result']['location']['lat']
    return lng, lat


if __name__ == '__main__':
    lon1, lat1, lon2, lat2 = 121.492009, 31.226894, 121.515526, 31.233206
    print("Azimuth", Azimuth(lon1, lat1, lon2, lat2))
    print("Azimuth", Azimuth(lon2, lat2, lon1, lat1))

    print(Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2))
    print("azimuthAngle", azimuthAngle(lon1, lat1, lon2, lat2))
