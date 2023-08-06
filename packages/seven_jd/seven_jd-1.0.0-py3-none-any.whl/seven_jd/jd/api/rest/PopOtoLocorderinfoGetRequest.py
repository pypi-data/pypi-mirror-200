# -*- coding: utf-8 -*-
"""
:Author: WangDe
:Date: 2023-02-07 17:42:06
:LastEditTime: 2023-02-07 17:43:01
:LastEditors: WangDe
:Description: 
"""
from seven_jd.jd.api.base import RestApi

class PopOtoLocorderinfoGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.order_id = None
			self.code_type = None			

		def getapiname(self):
			return 'jingdong.pop.oto.locorderinfo.get'

			





