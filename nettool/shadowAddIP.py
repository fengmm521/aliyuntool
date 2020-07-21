#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-07-20 15:39:21
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys
import json
import base64
import xmltool
#获取脚本路径

fileName = 'instance.txt'

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

def cmp(a,b):
    return ((a>b)-(a<b))

#获取父目录
def GetParentPath(strPath):
    if not strPath:
        return None;
    lsPath = os.path.split(strPath);
    if lsPath[1]:
        return lsPath[0];
    lsPath = os.path.split(lsPath[0]);
    return lsPath[0];

#获取目录下的所有类型文件
def getAllExtFile(pth,fromatx = ".erl"):
    jsondir = pth
    jsonfilelist = []
    for root, _dirs, files in os.walk(jsondir):
        for filex in files:          
            #print(filex)
            name,text = os.path.splitext(filex)
            if cmp(text,fromatx) == 0:
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
            elif fromatx == ".*" :
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
    return jsonfilelist


#获取一个目录下的所有子目录路径
def getAllDirs(spth):
    files = getAllExtFile(spth,'.*')
    makedirstmp = []
    isOK = True
    # 分析所有要创建的目录
    for d in files:
        if d[1] != '/' and (not d[1] in makedirstmp): #创建未创建的目录层级
            tmpdir = d[1][1:]
            tmpleves = tmpdir.split('/')
            alldirs = getAllLevelDirs(tmpleves)
            for dtmp in alldirs:
                if not dtmp in makedirstmp:
                    makedirstmp.append(dtmp)
    return makedirstmp
#获取目录下的所有文件路径
def getAllFiles(spth):
    files = getAllExtFile(spth,'.*')
    makedirstmp = []
    isOK = True
    # 分析所有要创建的目录
    for d in files:
        makedirstmp.append(d[0])
    return makedirstmp


def isFile(filename):
    try:
        with open(filename) as f:
            return True
    except IOError:
        return False


# ~/Library/Preferences/clowwindy.ShadowsocksX.plist 
def plistPth():
    cpth = cur_file_dir()
    pthdeep = 4
    for i in range(pthdeep):
        cpth = GetParentPath(cpth)
    tmppth = cpth + '/Library/Preferences/clowwindy.ShadowsocksX.plist'
    return tmppth
def getJsonConfig():
    cpth = cur_file_dir()
    pthdeep = 4
    for i in range(pthdeep):
        cpth = GetParentPath(cpth)
    tmppth = cpth + '/Documents/code/serverKey/x.json'
    return tmppth
def savePlistToXMLPth():
    cpth = cur_file_dir()
    pthdeep = 4
    for i in range(pthdeep):
        cpth = GetParentPath(cpth)
    tmppth = cpth + '/Documents/code/serverKey/x.xml'
    return tmppth
def keyPth():
    cpth = cur_file_dir()
    pthdeep = 4
    for i in range(pthdeep):
        cpth = GetParentPath(cpth)
    tmppth = cpth + '/Documents/code/serverKey'
    return tmppth

def changeJosnIP(tip):
    jpth = getJsonConfig()
    f = open(jpth,'r')
    dat = f.read()
    f.close()
    dicdat = json.loads(dat)
    # print(dicdat)
    password = ''
    for i,v in enumerate(dicdat['profiles']):
        print(v)
        if v['remarks'] == 'tserver':
            v['server'] = tip
            password = v['password']
        elif v['remarks'] == 'awsserver':
            v['server'] = tip
    # print(dicdat)
    json_str = json.dumps(dicdat)
    byte_res = base64.urlsafe_b64encode(bytes(json_str, "utf8"))
    # print(str(byte_res, "utf8"))
    return str(byte_res, "utf8"),password

def conventPlistToXML():
    pth = plistPth()
    # plutil -convert xml1 ~/Library/Preferences/clowwindy.ShadowsocksX.plist -o xxx.xml
    savepth = savePlistToXMLPth()
    cmd = '/usr/bin/plutil -convert xml1 %s -o %s'%(pth,savepth)
    os.system(cmd)

def cXML2Plist(xpth):
    pth = keyPth() + '/s.plist'
    # plutil -convert xml1 ~/Library/Preferences/clowwindy.ShadowsocksX.plist -o xxx.xml
    # -convert binary1 xxx.xml -o yyy.plist
    cmd = '/usr/bin/plutil -convert binary1 %s -o %s'%(xpth,pth)
    os.system(cmd)

    cmd = '/usr/bin/defaults import clowwindy.ShadowsocksX %s'%(pth)
    os.system(cmd)

def getIP(tip):
    ip = tip
    if not tip:
        pth = GetParentPath(cur_file_dir())
        fpth = pth + os.sep +fileName
        if os.path.exists(fpth):
            f = open(fpth,'r')
            jstr = f.read()
            f.close()
            dat = json.loads(jstr)
            print(dat)
            tkey = list(dat.keys())[0]
            ip = dat[tkey]
        else:
            print('not find the ip file...')
            return None
    return ip

def conventToXML(tip = None):
    ip = getIP(tip)
    base64str,password = changeJosnIP(ip)
    sxml = savePlistToXMLPth()
    xmltool.changeXML(sxml,ip,base64str,password)
    cXML2Plist(sxml)

# def conventPlist():
def main():
    conventToXML()

#测试
if __name__ == '__main__':
    main()
    
