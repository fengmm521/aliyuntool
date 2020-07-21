#!/usr/bin/env python
# coding=utf-8
#创建一个按量付费的云服务器
import json
import time
import traceback
import os

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from aliyunsdkecs.request.v20140526.RunInstancesRequest import RunInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
import getkey

RUNNING_STATUS = 'Running'
CHECK_INTERVAL = 3
CHECK_TIMEOUT = 180


class AliyunRunInstancesExample(object):

    def __init__(self):
        kid,ksec = getkey.getKeys()
        self.access_id = kid
        self.access_secret = ksec

        # 是否只预检此次请求。true：发送检查请求，不会创建实例，也不会产生费用；false：发送正常请求，通过检查后直接创建实例，并直接产生费用
        self.dry_run = False
        # 实例所属的地域ID
        self.region_id = 'cn-zhangjiakou'
        # 实例的资源规格
        self.instance_type = 'ecs.t6-c2m1.large'
        # 实例的计费方式
        self.instance_charge_type = 'PostPaid'
        # 镜像ID
        self.image_id = 'ubuntu_18_04_x64_20G_alibase_20200618.vhd'
        # 指定新创建实例所属于的安全组ID
        self.security_group_id = 'sg-8vb6jluk3qc318f2ek0t'
        # 购买资源的时长
        self.period = 1
        # 购买资源的时长单位
        self.period_unit = 'Hourly'
        # 实例所属的可用区编号
        self.zone_id = 'cn-zhangjiakou-a'
        # 网络计费类型
        self.internet_charge_type = 'PayByTraffic'
        # 虚拟交换机ID
        self.vswitch_id = 'vsw-8vbeb7jtt62w65vcze0hz'
        # 实例名称
        self.instance_name = 'launch-advisor-20200718'
        # 指定创建ECS实例的数量
        self.amount = 1
        # 公网出带宽最大值
        self.internet_max_bandwidth_out = 5
        # 云服务器的主机名
        self.host_name = 'DL01'
        # 是否为I/O优化实例
        self.io_optimized = 'optimized'
        # 密钥对名称
        self.key_pair_name = 'mageKey'
        # 是否开启安全加固
        self.security_enhancement_strategy = 'Active'
        # 系统盘大小
        self.system_disk_size = '40'
        # 系统盘的磁盘种类
        self.system_disk_category = 'cloud_efficiency'
        
        self.client = AcsClient(self.access_id, self.access_secret, self.region_id)

        self.instances = {}

    def run(self):
        try:
            ids = self.run_instances()
            self._check_instances_status(ids)
        except ClientException as e:
            print('Fail. Something with your connection with Aliyun go incorrect.'
                  ' Code: {code}, Message: {msg}'
                  .format(code=e.error_code, msg=e.message))
        except ServerException as e:
            print('Fail. Business error.'
                  ' Code: {code}, Message: {msg}'
                  .format(code=e.error_code, msg=e.message))
        except Exception:
            print('Unhandled error')
            print(traceback.format_exc())

    def run_instances(self):
        """
        调用创建实例的API，得到实例ID后继续查询实例状态
        :return:instance_ids 需要检查的实例ID
        """
        request = RunInstancesRequest()
       
        request.set_DryRun(self.dry_run)
        
        request.set_InstanceType(self.instance_type)
        request.set_InstanceChargeType(self.instance_charge_type)
        request.set_ImageId(self.image_id)
        request.set_SecurityGroupId(self.security_group_id)
        request.set_Period(self.period)
        request.set_PeriodUnit(self.period_unit)
        request.set_ZoneId(self.zone_id)
        request.set_InternetChargeType(self.internet_charge_type)
        request.set_VSwitchId(self.vswitch_id)
        request.set_InstanceName(self.instance_name)
        request.set_Amount(self.amount)
        request.set_InternetMaxBandwidthOut(self.internet_max_bandwidth_out)
        request.set_HostName(self.host_name)
        request.set_IoOptimized(self.io_optimized)
        request.set_KeyPairName(self.key_pair_name)
        request.set_SecurityEnhancementStrategy(self.security_enhancement_strategy)
        request.set_SystemDiskSize(self.system_disk_size)
        request.set_SystemDiskCategory(self.system_disk_category)
         
        body = self.client.do_action_with_exception(request)
        data = json.loads(body)
        instance_ids = data['InstanceIdSets']['InstanceIdSet']
        print('Success. Instance creation succeed. InstanceIds: {}'.format(', '.join(instance_ids)))
        return instance_ids

    def _check_instances_status(self, instance_ids):
        """
        每3秒中检查一次实例的状态，超时时间设为3分钟。
        :param instance_ids 需要检查的实例ID
        :return:
        """
        start = time.time()
        while True:
            request = DescribeInstancesRequest()
            request.set_InstanceIds(json.dumps(instance_ids))
            body = self.client.do_action_with_exception(request)
            data = json.loads(body)
            for instance in data['Instances']['Instance']:
                if RUNNING_STATUS in instance['Status']:
                    instance_ids.remove(instance['InstanceId'])
                    print('Instance boot successfully: {}'.format(instance['InstanceId']))
                    if 'PublicIpAddress' in instance and len(instance['PublicIpAddress']['IpAddress']) > 0:
                        self.instances[instance['InstanceId']] = instance['PublicIpAddress']['IpAddress'][0]
                        # self.publicIPs.append(instance['InstanceId']['IpAddress'][0])

            if not instance_ids:
                print('Instances all boot successfully')
                break

            if time.time() - start > CHECK_TIMEOUT:
                print('Instances boot failed within {timeout}s: {ids}'
                      .format(timeout=CHECK_TIMEOUT, ids=', '.join(instance_ids)))
                break

            time.sleep(CHECK_INTERVAL)
#DescribeInstancesRequest返回结果
# {
#     "Instances": {
#         "Instance": [
#             {
#                 "ResourceGroupId": "",
#                 "Memory": 1024,
#                 "InstanceChargeType": "PostPaid",
#                 "Cpu": 2,
#                 "OSName": "Ubuntu  18.04 64位",
#                 "InstanceNetworkType": "vpc",
#                 "InnerIpAddress": {
#                     "IpAddress": []
#                 },
#                 "ExpiredTime": "2099-12-31T15:59Z",
#                 "ImageId": "ubuntu_18_04_x64_20G_alibase_20200618.vhd",
#                 "EipAddress": {
#                     "AllocationId": "",
#                     "IpAddress": "",
#                     "InternetChargeType": ""
#                 },
#                 "HostName": "DL01",
#                 "VlanId": "",
#                 "Status": "Running",
#                 "MetadataOptions": {
#                     "HttpTokens": "",
#                     "HttpEndpoint": ""
#                 },
#                 "InstanceId": "i-8vb4p36x0b4gqhgd7fzk",
#                 "StoppedMode": "Not-applicable",
#                 "CpuOptions": {
#                     "ThreadsPerCore": 2,
#                     "Numa": "",
#                     "CoreCount": 1
#                 },
#                 "StartTime": "2020-07-18T03:48Z",
#                 "DeletionProtection": false,
#                 "SecurityGroupIds": {
#                     "SecurityGroupId": [
#                         "sg-8vb6jluk3qc318f2ek0t"
#                     ]
#                 },
#                 "VpcAttributes": {
#                     "PrivateIpAddress": {
#                         "IpAddress": [
#                             "192.168.1.197"
#                         ]
#                     },
#                     "VpcId": "vpc-8vb2zt8lnk9cmr09c14hu",
#                     "VSwitchId": "vsw-8vbeb7jtt62w65vcze0hz",
#                     "NatIpAddress": ""
#                 },
#                 "InternetChargeType": "PayByTraffic",
#                 "InstanceName": "launch-advisor-20200718",
#                 "DeploymentSetId": "",
#                 "InternetMaxBandwidthOut": 5,
#                 "SerialNumber": "7e314162-f666-452b-b888-5dce1c8a8b74",
#                 "OSType": "linux",
#                 "CreationTime": "2020-07-18T03:48Z",
#                 "AutoReleaseTime": "",
#                 "Description": "",
#                 "InstanceTypeFamily": "ecs.t6",
#                 "DedicatedInstanceAttribute": {
#                     "Tenancy": "",
#                     "Affinity": ""
#                 },
#                 "PublicIpAddress": {
#                     "IpAddress": [
#                         "39.99.202.191"
#                     ]
#                 },
#                 "GPUSpec": "",
#                 "NetworkInterfaces": {
#                     "NetworkInterface": [
#                         {
#                             "PrimaryIpAddress": "192.168.1.197",
#                             "NetworkInterfaceId": "eni-8vbd5s5zengj2q797d0u",
#                             "MacAddress": "00:16:3e:0e:71:31"
#                         }
#                     ]
#                 },
#                 "SpotPriceLimit": 0,
#                 "DeviceAvailable": true,
#                 "SaleCycle": "",
#                 "InstanceType": "ecs.t6-c2m1.large",
#                 "OSNameEn": "Ubuntu  18.04 64 bit",
#                 "SpotStrategy": "NoSpot",
#                 "KeyPairName": "mageKey",
#                 "IoOptimized": true,
#                 "ZoneId": "cn-zhangjiakou-a",
#                 "ClusterId": "",
#                 "EcsCapacityReservationAttr": {
#                     "CapacityReservationPreference": "",
#                     "CapacityReservationId": ""
#                 },
#                 "DedicatedHostAttribute": {
#                     "DedicatedHostId": "",
#                     "DedicatedHostName": ""
#                 },
#                 "GPUAmount": 0,
#                 "OperationLocks": {
#                     "LockReason": []
#                 },
#                 "InternetMaxBandwidthIn": 80,
#                 "Recyclable": false,
#                 "RegionId": "cn-zhangjiakou",
#                 "CreditSpecification": "Standard"
#             }
#         ]
#     },
#     "TotalCount": 1,
#     "RequestId": "282DCB52-1494-4B92-94AB-F72B0D3997E4",
#     "PageSize": 10,
#     "PageNumber": 1
# }
# Success. Instance creation succeed. InstanceIds: i-8vb4p36x0b4gqhgd7fzk
# Instance boot successfully: i-8vb4p36x0b4gqhgd7fzk
# Instances all boot successfully
fileName = 'instance.txt'
def createECS():
    tmp = AliyunRunInstancesExample()
    tmp.run()
    print(tmp.instances)
    return tmp.instances

def getStr2Json(pdic):
    jstr = json.dumps(pdic)
    return jstr

def main():
    if os.path.exists(fileName):
        print('instance is exists!')
        return
    tmp = AliyunRunInstancesExample()
    tmp.run()
    print(tmp.instances)
    jstr = getStr2Json(tmp.instances)
    f = open(fileName,'w')
    f.write(jstr)
    f.close()
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')
    time.sleep(1)
    print('the server is start.....')
if __name__ == '__main__':
    main()
    