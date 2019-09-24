#!/usr/bin/env python
#coding=utf-8

#注意，程序只支持python3
#查询镜像资源

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeImagesRequest import DescribeImagesRequest


import configtool

import json

import pprint

accKey,accSec = configtool.getCSVConfigData()

client = AcsClient(accKey, accSec, 'ap-south-1')

request = DescribeImagesRequest()
request.set_accept_format('json')
#系统架构
request.set_Architecture("x86_64")
#镜像使用场景
request.set_ActionType('CreateEcs')
#镜像来源,system:公共镜像
request.set_ImageOwnerAlias('system')
#单页最大显示数量
request.set_PageSize(10)
#显示页码
# request.set_PageNumber(4)
#指定实例类型
request.set_InstanceType('ecs.t5-lc2m1.nano')
#镜像是否可以运行在I/O优化实例上
request.set_IsSupportIoOptimized(True)
#镜像操作系统类型
request.set_OSType('linux')
#镜像ID
# request.set_ImageId('ubuntu')
#过滤键值
request.set_Filters([
  {
    "Key": "Platform",
    "Value": "Ubuntu"
  }
])

response = client.do_action_with_exception(request)
# python2:  print(response) 
# print(str(response, encoding='utf-8'))
jstr = str(response, encoding='utf-8')

jdat = json.loads(jstr)

#格式化输出dict字典,自定义缩进为4空格
# pp = pprint.PrettyPrinter(indent=2)
pp = pprint.PrettyPrinter()
pp.pprint(jdat)

#ubuntu_18_04_64_20G_alibase_20190624.vhd,这个是常用的ubuntu18.04的镜像ID
