#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os
while True:
    time.sleep(10800) #3小时=10800秒
    tmp = os.popen('sh free.sh').readlines()
    for s in tmp:
        print s
