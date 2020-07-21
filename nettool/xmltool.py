#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-07-20 15:39:21
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
# import xml.etree.ElementTree as ET


def changeXML(sxml,tip,dat,psd):
    xmlstr = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PBS</key>
    <string>Copv9p5PRHLeK66opkTUkg/nOAlBLd9A3+659k/x3nUmz2O1HoVxtuxOjhRzVzNG</string>
    <key>ShadowsocksIsRunning</key>
    <true/>
    <key>ShadowsocksMode</key>
    <string>global</string>
    <key>config</key>
    <data>
    %s
    </data>
    <key>proxy encryption</key>
    <string>aes-256-cfb</string>
    <key>proxy ip</key>
    <string>%s</string>
    <key>proxy password</key>
    <string>%s</string>
    <key>proxy port</key>
    <string>8189</string>
    <key>public server</key>
    <false/>
</dict>
</plist>
'''%(dat,tip,psd)
    f = open(sxml,'w') 
    f.write(xmlstr)
    f.close()
    
# ————————————————
# 版权声明：本文为CSDN博主「Webben」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/Webben/article/details/84787888
    
def main():
    # changeXML('/Users/mage/Documents/code/serverKey/xxx.xml', 'aaabbbccc')
    pass

#测试
if __name__ == '__main__':
    main()
    
