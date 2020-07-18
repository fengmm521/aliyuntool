#!/usr/bin/env python
#coding=utf-8

#获取实例信息,私网公网IP什么的
#下边是返回的结果
# {
#   "Description": "",
#   "Memory": 1024,
#   "InstanceChargeType": "PostPaid",
#   "Cpu": 2,
#   "InstanceNetworkType": "vpc",
#   "PublicIpAddress": {
#     "IpAddress": [
#       "39.99.202.191"
#     ]
#   },
#   "InnerIpAddress": {
#     "IpAddress": [
      
#     ]
#   },
#   "ExpiredTime": "2099-12-31T15:59Z",
#   "ImageId": "ubuntu_18_04_x64_20G_alibase_20200618.vhd",
#   "EipAddress": {
#     "AllocationId": "",
#     "IpAddress": "",
#     "InternetChargeType": ""
#   },
#   "InstanceType": "ecs.t6-c2m1.large",
#   "HostName": "DL01",
#   "VlanId": "",
#   "Status": "Running",
#   "IoOptimized": "optimized",
#   "RequestId": "EBAC43A4-F270-4C80-8C0A-3ED5735008C6",
#   "ZoneId": "cn-zhangjiakou-a",
#   "InstanceId": "i-8vb4p36x0b4gqhgd7fzk",
#   "ClusterId": "",
#   "StoppedMode": "Not-applicable",
#   "DedicatedHostAttribute": {
#     "DedicatedHostId": "",
#     "DedicatedHostName": ""
#   },
#   "SecurityGroupIds": {
#     "SecurityGroupId": [
#       "sg-8vb6jluk3qc318f2ek0t"
#     ]
#   },
#   "VpcAttributes": {
#     "PrivateIpAddress": {
#       "IpAddress": [
#         "192.168.1.197"
#       ]
#     },
#     "VpcId": "vpc-8vb2zt8lnk9cmr09c14hu",
#     "VSwitchId": "vsw-8vbeb7jtt62w65vcze0hz",
#     "NatIpAddress": ""
#   },
#   "OperationLocks": {
#     "LockReason": [
      
#     ]
#   },
#   "InternetChargeType": "PayByTraffic",
#   "InstanceName": "launch-advisor-20200718",
#   "InternetMaxBandwidthOut": 5,
#   "InternetMaxBandwidthIn": 80,
#   "SerialNumber": "7e314162-f666-452b-b888-5dce1c8a8b74",
#   "CreationTime": "2020-07-18T03:48:23Z",
#   "RegionId": "cn-zhangjiakou",
#   "CreditSpecification": "Standard"
# }
#https://api.aliyun.com/#/?product=Ecs&version=2014-05-26&api=DescribeInstanceAttribute&tab=DEMO&lang=PYTHON
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstanceAttributeRequest import DescribeInstanceAttributeRequest

import getkey
import os

fileName = 'instance.txt'

def getIntanceID():
    if os.path.exists(fileName):
        f = open(fileName,'r')
        jstr = f.read()
        f.close()
        dat = json.loads(jstr)
        return dat
    return None

def main():
    dat = getIntanceID()
    print(dat)
    if dat:
        instanceID = dat.keys()[0]
        kid,ksec = getkey.getKeys()

        client = AcsClient(kid, ksec, 'cn-zhangjiakou')

        request = DescribeInstanceAttributeRequest()
        request.set_accept_format('json')

        request.set_InstanceId(instanceID)

        response = client.do_action_with_exception(request)
        # python2:  print(response) 
        print(str(response, encoding='utf-8'))
if __name__ == '__main__':
    main()
