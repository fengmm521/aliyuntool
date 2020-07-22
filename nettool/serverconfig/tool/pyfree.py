#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os
import sys
#获取脚本路径
def cur_file_dir():
    pathx = sys.argv[0]
    tmppath,_file = os.path.split(pathx)
    if cmp(tmppath,'') == 0:
        tmppath = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(tmppath):
        return tmppath
    elif os.path.isfile(tmppath):
        return os.path.dirname(tmppath)
freepth = cur_file_dir() + os.sep +'free.sh'
cmd = '/bin/sh %s'%(freepth)
while True:
    time.sleep(10800) #3小时=10800秒
    tmp = os.popen(cmd).readlines()
    for s in tmp:
        print s
