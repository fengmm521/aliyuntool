#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-07-20 12:26:56
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys
import paramiko
import json
import shadowAddIP
import time

fileName = 'instance.txt'
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

def finddir(arg,dirname,filenames):
    name,text = os.path.split(dirname)
    dirnametmp = str(dirname)
    if text and text[0] == '.':
        print(dirname)
        print(filenames)
        os.system('rm -r %s'%(dirname))
        return
    elif filenames:
        for f in filenames:
            if f[0] == '.' and isFile(dirname + f):
                fpthtmp = dirname + f
                if f.find(' '):
                    nf = f.replace(' ','\ ')
                    fpthtmp = dirname + nf
                print(dirname + f)
                os.system('rm  %s'%(fpthtmp))

#删除所有pth目录下的所有"."开头的文件名和目录名
def removeProjectAllHideDir(pth):
    alldirs = getAllDirs(pth)
    if not ('/' in alldirs):
        alldirs.append('/')
    for d in alldirs:
        tmpth = pth + d
        os.path.walk(tmpth, finddir, 0)

#获取一个路径中所包含的所有目录及子目录
def getAllLevelDirs(dirpths):
    dirleves = []
    dirtmp = ''
    for d in dirpths:
        dirtmp += '/' + d
        dirleves.append(dirtmp)
    return dirleves

#在outpth目录下创建ndir路径中的所有目录，是否使用决对路径
def makeDir(outpth,ndir):
    tmpdir = ''
    if ndir[0] == '/':
        tmpdir = outpth + ndir
    else:
        tmpdir = outpth + '/' + ndir
    print(tmpdir)
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)

# 创建一个目录下的所有子目录到另一个目录
def createDirs(spth,tpth):
    files = getAllExtFile(spth,'.*')
    makedirstmp = []
    isOK = True
    # 分析所有要创建的目录
    tmpfpth = fpth
    for d in files:
        if d[1] != '/' and (not d[1] in makedirstmp): #创建未创建的目录层级
            tmpdir = d[1][1:]
            tmpleves = tmpdir.split('/')
            alldirs = getAllLevelDirs(tmpleves)
            for dtmp in alldirs:
                if not dtmp in makedirstmp:
                    makeDir(tpth,dtmp)
                    makedirstmp.append(dtmp)

# 替换文件名
def replaceFileName(path,sname,replaceStr,tostr):
    a = sname
    tmpname = a.replace(replaceStr, tostr)
    outpath = path + tmpname
    oldpath = path + sname
    cmd = "mv %s %s"%(oldpath,outpath)
    print(cmd)
    os.system("mv %s %s"%(oldpath,outpath))

# 替换目录下的文件名中某个字符串为其他字符串
def renameDir(sdir,replacestr,tostr,exittype):
    files = getAllExtFile(sdir,fromatx = exittype)
    allfilepath = []
    for f in files:
        tmppath = sdir + f[1]
        filename = f[2] + exittype
        allfilepath.append([tmppath,filename])
    for p in allfilepath:
        replaceFileName(p[0], p[1], replacestr, tostr)

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

def getKeyFilePth():
    cpth = cur_file_dir()
    pthdeep = 4
    for i in range(pthdeep):
        cpth = GetParentPath(cpth)
    fpth = cpth + os.sep + '.ssh' + os.sep +'id_rsa'
    return fpth

def openSSH(tip,uname):
    #创建ssh客户端
    client = paramiko.SSHClient()
    #第一次ssh远程时会提示输入yes或者no
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #密码方式远程连接
    # client.connect(sys_ip, 22, username=username, password=password, timeout=20)
    #互信方式远程连接
    keyPth = getKeyFilePth()
    key_file = paramiko.RSAKey.from_private_key_file(keyPth)
    ip = getIP(tip)
    client.connect(ip, 22, username=uname, pkey=key_file, timeout=20)
    return client
def closeSSH(ssh):
    if ssh:
        ssh.close()

# 上传文件
def sftp_upload_file(local_path,server_path,tip = None,uname='root'):
    try:
        ssh = openSSH(tip, uname)
        t = ssh.get_transport()
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
    except Exception as  e:
        print(e)

# 下载文件
def sftp_down_file(local_path,server_path,tip = None,uname='root'):
    try:
        ssh = openSSH(tip, uname)
        t = ssh.get_transport()
        sftp=paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
    except Exception as e:
        print(e)

#远程登陆操作系统
def sshcmd(cmds,tip = None,uname = 'root'):
    client = None
    try:
        client = openSSH(tip, uname)
        #执行命令
        allresult = []
        for i,v in enumerate(cmds):
            print('start run cmd:%s'%(v))
            stdin, stdout, stderr = client.exec_command(v)
            #获取命令执行结果,返回的数据是一个list
            result = stdout.readlines()
            print(result)
            allresult.append(result)
            time.sleep(0.5) #延时等0.5秒后再进行下一条指令
        return allresult
        client.close()
    except Exception as e:
        print(e)
    finally:
        if client:
            client.close()

def scpResToServer(local_path,server_path,tip = None,uname = 'root'):
    if not os.path.exists(local_path):
        print('local_path not exists:%s'%(local_path))
        return
    ip = getIP(tip)
    if isFile(local_path):
        # print('start upload file:%s\n to server pth:%s'%(local_path,server_path))
        cmd = '/usr/bin/scp ' + local_path + ' ' + uname + '@' + ip + ':' + server_path
        print(cmd)
        os.system(cmd)
    else:
        # print('start upload dir:%s\n to server pth:%s'%(local_path,server_path))
        cmd = '/usr/bin/scp -r ' + local_path + ' ' + uname + '@' + ip + ':' + server_path
        print(cmd)
        os.system(cmd)

def scpResFromServer(local_path,server_path,tip = None,uname = 'root'):
    if not os.path.exists(local_path):
        print('local_path not exists:%s'%(local_path))
        return
    ip = getIP(tip)
    if isFile(local_path):
        # print('start download file:%s\n from server pth:%s'%(local_path,server_path))
        cmd = '/usr/bin/scp ' + uname + '@' + ip + ':' + server_path + ' ' +local_path 
        print(cmd)
        os.system(cmd)
    else:
        # print('start download dir:%s\n from server pth:%s'%(local_path,server_path))
        cmd = '/usr/bin/scp -r ' + uname + '@' + ip + ':' + server_path + ' ' +local_path 
        print(cmd)
        os.system(cmd)

def uploadSSServer():
    cpth = cur_file_dir()
    pthdeep = 4
    for i in range(pthdeep):
        cpth = GetParentPath(cpth)
    local_path = cpth + '/Documents/code/serverKey/shadowsocks'
    server_path = '/root'
    print(local_path)
    print(server_path)
    scpResToServer(local_path, server_path)

def uploadHaproxy():
    cpth = cur_file_dir()
    pthdeep = 4
    for i in range(pthdeep):
        cpth = GetParentPath(cpth)
    local_path = cpth + '/Documents/code/serverKey/haproxy'
    server_path = '/root'
    print(local_path)
    print(server_path)
    scpResToServer(local_path, server_path)

def uploadSHell():
    cpth = cur_file_dir()
    pthdeep = 4
    for i in range(pthdeep):
        cpth = GetParentPath(cpth)
    local_path = cpth + '/Documents/code/serverKey/startserver'
    server_path = '/root'
    print(local_path)
    print(server_path)
    scpResToServer(local_path, server_path)

def uploadTools():
    cpth = cur_file_dir()
    pthdeep = 4
    for i in range(pthdeep):
        cpth = GetParentPath(cpth)
    local_path = cpth + '/Documents/code/serverKey/tool'
    server_path = '/root'
    print(local_path)
    print(server_path)
    scpResToServer(local_path, server_path)

def runSHell():
    cmds = ['/bin/sh /root/startserver','/bin/ps -A|grep ssserver','/bin/ps -A|grep haproxy']
    backs = sshcmd(cmds)
    for i,v in enumerate(backs):
        print(v)

def changeLocalSSServerIP():
    tip = getIP()
    if tip:
        shadowAddIP.conventToXML(tip)
    else:
        print('the not heave create server ip')

def main():
    # kpth = getKeyFilePth()
    ip = getIP()
    if ip:
        cmds = ['pwd']
        backs = sshcmd(cmds)
        print(backs)
        uploadSSServer()
        uploadHaproxy()
        uploadSHell()
        uploadTools()
        runSHell()
    else:
        print('not find server ip file:instance.txt')
    # changeLocalSSServerIP()

def test():
    kpth = getKeyFilePth()
    print(kpth)
    print(sys.path)

if __name__=="__main__":
    main()
