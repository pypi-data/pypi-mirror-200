# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2023-04-03 14:45:49
:LastEditTime: 2023-04-03 14:51:13
:LastEditors: HuangJingCan
:Description: 
"""
from seven_jd.jd.api.base import sign


class appinfo(object):
    def __init__(self, appkey, secret):
        self.appkey = appkey
        self.secret = secret


def getDefaultAppInfo():
    pass


def setDefaultAppInfo(appkey, secret):
    default = appinfo(appkey, secret)
    global getDefaultAppInfo
    getDefaultAppInfo = lambda: default
