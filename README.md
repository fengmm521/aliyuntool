# 阿里云云服务器python创建api例子

使用前要先使用pip安装python的云服务器SDK

https://github.com/aliyun/aliyun-openapi-python-sdk

```bash
# Install the core library
 pip install aliyun-python-sdk-core
 # Install the ECS management library
 pip install aliyun-python-sdk-ecs
 # Install the RDS management library
 pip install aliyun-python-sdk-rds
```

调用api先需要申请api密鉏key和密鉏值，在控制台RAM访问控制处设置

https://ram.console.aliyun.com/overview

给不同用户不同的访问权限以增加安全性

## 使用时的一些注意事项

1. 创建实例前先要建好VPC虚拟专用网络和虚拟交换机，因为在创建时需要用到虚拟交换机ID(VSwitchId)
2. 要先在镜像市场或者公共镜像处找到实例的系统盘镜像ID，这个在创健实例时也会用到(ImageId)
3. 可以手动或者调用api创建好网络安全组,得到安全组ID (SecurityGroupId)
4. 如果为了安全要使用密钥对登陆服务器，也要提前设置或者建好密钥对得到ID,或者使用密码
5. 正式使用api创建实例前可以先设置DryRun为True测试api是否参好参数并可以使用
6. 创建实例前要先查换好要创建的实例硬件配置类型ID，主要是CPU和内存，拿到类型ID(InstanceType)

最后，如果使用密码登陆，要使用https请求，官方建意，最好还是使用密钥对

createECS.py

这个文件是创建一个有公网IP的按量计费ecs服务器,

DeleteECS.py

这个文件是删除一个已创建的云服务器

ECSInfo.py

这个文件是显示已创建的服务器信息

nettool

这个目录下放的是配置云服务器的相关脚本和工具

## 工具使用方法

``` bash
#创建一个云服务器
ecstool open 	
#删除一个云服务器
ecstool close 	
#上传服务器工具用启动一个转发服务器程序和一个ssserver服务器,并且同时更新本地客户端的服务器地址
ecstool server  
```
