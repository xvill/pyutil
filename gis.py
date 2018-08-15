# -*- coding: utf-8 -*-

import requests


def AmapGeocode(ak, address):
    """gaodeAPI:根据传入地名参数获取经纬度"""
    res = requests.get("http://restapi.amap.com/v3/geocode/geo",
                       params={'address': address, 'key': ak}).json()
    lng, lat = 0, 0
    if res["info"] == 'OK':
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
