#!/usr/bin/env python
# coding=utf-8
import os,sys

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

#'~/Documents/code/key/aliyunkey/20200718103047.csv'
def getFilePth():
    cpth = cur_file_dir()
    #Documents/github/aliyuntool
    fpth = GetParentPath(GetParentPath(cpth)) + os.sep + "code/key/aliyunkey/20200718103047.csv"
    #Documents/code/key/aliyunkey/20200718103047.csv
    print(fpth)
    return fpth
def getKeys():
    KeyPTH = getFilePth()
    f = open(KeyPTH,'r')
    lines = f.readlines()
    f.close()
    print(lines[0][:-1])
    print(lines[1][:-1])
    ktmp = lines[1].replace('\n','').replace('\t','').replace('\r','').replace(' ','')
    ks = ktmp.split(',')
    keyid = ks[0][1:-1]
    keyval = ks[1][1:-1]
    print(keyid)
    print(keyval)
    return keyid,keyval

def main():
    getKeys()

if __name__ == '__main__':
    main()