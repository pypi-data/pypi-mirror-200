# PaasSdk-Python

#### 介绍
融营智能Python SDK是官方软件开发工具包。它使您的Python应用程序、库或脚本与融营智能服务集成变得很容易。

此模块适用于Python版本:

3及以上版本
#### 软件架构
融营智能 python Sdk


#### 安装教程

1.  pip install RongyingPaasSdk==1.1.2


#### 使用说明

1.  引用Sdk组件


            from PaasSdk.CreateRequestClient import CreateRequestClient as Client
            from PaasSdk.Config import Config as Config
            from PaasSdk import RequestModel as models

2.  调用方法

    
            config = Config(AccountSid='您的账户Sid',                                    
                            AccountToken='您的账户Token')                                
            client = Client(config)                    
            request = models.CreateApplicationsRequestModel(AppName="python测试") 
            info = client.CreateApplications(request)
    




