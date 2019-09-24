#!/usr/bin/env python
#coding=utf-8

#注意，程序只支持python3

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeAvailableResourceRequest import DescribeAvailableResourceRequest


import configtool

import json

import pprint

accKey,accSec = configtool.getCSVConfigData()

client = AcsClient(accKey, accSec, 'ap-south-1')

request = DescribeAvailableResourceRequest()
request.set_accept_format('json')

request.set_DestinationResource("InstanceType")
request.set_Cores(1)
# request.set_InstanceType('ecs.t5-lc2m1.nano')

response = client.do_action_with_exception(request)
# python2:  print(response) 
# print(str(response, encoding='utf-8'))
jstr = str(response, encoding='utf-8')

jdat = json.loads(jstr)

#格式化输出dict字典,自定义缩进为4空格
# pp = pprint.PrettyPrinter(indent=2)
pp = pprint.PrettyPrinter()
pp.pprint(jdat)
