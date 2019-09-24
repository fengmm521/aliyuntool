#!/usr/bin/env python
#coding=utf-8

#注意，程序只支持python3
#创建安全组

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.CreateSecurityGroupRequest import CreateSecurityGroupRequest


import configtool

import json

import pprint

accKey,accSec = configtool.getCSVConfigData()

client = AcsClient(accKey, accSec, 'ap-south-1')

request = CreateSecurityGroupRequest()
request.set_accept_format('json')

#安全组描述
request.set_Description("mm_sstest")
#安装组名称
request.set_SecurityGroupName("mm_sstest")
#安全组专有网络ID
request.set_VpcId("vpc-a2d3oq2uakxv0vb38hhcm")

response = client.do_action_with_exception(request)
# python2:  print(response) 
# print(str(response, encoding='utf-8'))
jstr = str(response, encoding='utf-8')

jdat = json.loads(jstr)

#格式化输出dict字典,自定义缩进为4空格
# pp = pprint.PrettyPrinter(indent=2)
pp = pprint.PrettyPrinter()
pp.pprint(jdat)

