#!/usr/bin/env python
#coding=utf-8

#https://api.aliyun.com/#/?product=Ecs&version=2014-05-26&api=DeleteInstance&tab=DEMO&lang=PYTHON

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DeleteInstanceRequest import DeleteInstanceRequest
import getkey
import os
import json

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
    # print(list(dat.keys()))
    if dat:
        instanceID = list(dat.keys())[0]
        kid,ksec = getkey.getKeys()
        client = AcsClient(kid, ksec, 'cn-zhangjiakou')

        request = DeleteInstanceRequest()
        request.set_accept_format('json')

        request.set_InstanceId(instanceID)
        request.set_Force(True)

        response = client.do_action_with_exception(request)
        # python2:  print(response) 
        print(str(response, encoding='utf-8'))
        rdic = json.loads(response)
        if 'RequestId' in rdic:
            os.remove(fileName)
    else:
        print('not heave instance!')
#返回结果
# {"RequestId":"D525A436-922F-476C-8A02-D19D6068A396"}

#下边为自动释放api:
#https://api.aliyun.com/#/?product=Ecs&version=2014-05-26&api=ModifyInstanceAutoReleaseTime&params={"RegionId":"cn-zhangjiakou"}&tab=DEMO&lang=PYTHON

if __name__ == '__main__':
    main()
