#!/usr/bin/env python
#coding=utf-8

#注意，程序只支持python3
#创建印度孟买按量计费实例

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.CreateInstanceRequest import CreateInstanceRequest



import configtool

import json

import pprint

accKey,accSec = configtool.getCSVConfigData()

client = AcsClient(accKey, accSec, 'ap-south-1')

request = CreateInstanceRequest()
request.set_accept_format('json')

#使用的系统镜像为ubuntu 18.04
request.set_ImageId("ubuntu_18_04_64_20G_alibase_20190624.vhd")#ubuntu_18_04_64_20G_alibase_20190624.vhd
#使用的云服务器类型为入门型，限制CPU实例
request.set_InstanceType("ecs.t5-lc2m1.nano")#ecs.t5-lc2m1.nano
#VPC实例专有网络要设置VSwitchId,必选项
request.set_VSwitchId('vsw-a2d0lu4o1qpnijlgfig92')
#使用的安全组名称
request.set_SecurityGroupId("sg-a2d0p0b52kp56uc52ac3")
#设置的实例名称
request.set_InstanceName("mm_ss2")
#设置为网络按量付费
request.set_InternetChargeType("PayByTraffic")
# #设置主机名
request.set_HostName("LocalHost001") #不设置则默认可能是root
# #登陆密码，建意使用https发送请求，最好使用密钥登陆，使用密钥登陆时则会禁止密码登陆系统
request.set_Password("7654123Hh33")
# #选择地服务器区组
request.set_ZoneId("ap-south-1a")       #实例所在区组一定要和虚拟交换机匹配，要不然会找不到可以交换机
# #设置创建服务器实例的唯一ID
#request.set_ClientToken("creartEcs-mm99")
# #实例系统系大小，单位为GB
request.set_SystemDiskSize(40)
# #实例系统盘类型，cloud为高效云盘
request.set_SystemDiskCategory("cloud_efficiency")
# #系统盘名称
request.set_SystemDiskDiskName("system")
# #系统盘描述
request.set_SystemDiskDescription("system_pan")
# #设置实例为按量付费
request.set_InstanceChargeType("PostPaid")
# #是否测试运行api,当是true时不会真正创建实例，只会验证api是否调用正确
request.set_DryRun(True)
#实例是否可通过控制台或者API释放
# request.set_DeletionProtection(True)

response = client.do_action_with_exception(request)
# python2:  print(response) 
# print(str(response, encoding='utf-8'))
jstr = str(response, encoding='utf-8')

jdat = json.loads(jstr)

#格式化输出dict字典,自定义缩进为4空格
# pp = pprint.PrettyPrinter(indent=2)
pp = pprint.PrettyPrinter()
pp.pprint(jdat)

