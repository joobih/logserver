#!/usr/bin/env python
# coding=utf-8

import sys,os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'submodules'))

import ConfigParser
from Common.queues.rb_product import RQProduct

"""
    单例模式下的log_client
"""
class LogClient(object):

    __instance = None    

    def __new__(cls,*args,**kwd):
        print "__new__"
        if LogClient.__instance is None:
            LogClient.__instance=object.__new__(cls,*args,**kwd)
        return LogClient.__instance

    """
        log_name:需要发送日志的服务名字，最后会以该参数为文件名存放在对应的project_queue文件夹下面
        project_queue:项目队列名称，该参数也是rabbitmq队列名称，应该是一个大的项目统一使用一个名称作为日志队列。最后日志文件以project_queue为文件夹存放
        rq_host:rabbitmq 服务器地址
        rq_port:rabbitmq 服务器端口号
    """
    def init(self,log_name,project_queue,rq_host="127.0.0.1",rq_port=5672):
        print "__init__",log_name
        self.log_name = log_name
        self.product = RQProduct(project_queue,rq_host,rq_port)
 
    def __init__(self):
        pass

    def info(self,data):
        msg = {"log_name":self.log_name,"level":"info","logs":data}
        self.product.product(msg)

    def debug(self,data):
        msg = {"log_name":self.log_name,"level":"debug","logs":data}
        self.product.product(msg)
        
    def error(self,data):
        msg = {"log_name":self.log_name,"level":"error","logs":data}
        self.product.product(msg)

    def warn(self,data):
        msg = {"log_name":self.log_name,"level":"warn","logs":data}
        self.product.product(msg)

if __name__ == "__main__":
    conf = ConfigParser.ConfigParser()
    conf.read("setting.conf")
    log_name = "log_server"
    rq_queue = conf.get("rabbitmq","queue")
    rq_host = conf.get("rabbitmq","host") 
    rq_port = conf.get("rabbitmq","port")
    LogClient().init(log_name,rq_queue,rq_host,rq_port)
    logger = LogClient()
    print logger,type(logger)
    msg = "Now i send a msg to you info"
    LogClient().info(msg)
    logger.debug(msg)
    logger.error(msg)
    logger.warn(msg)
    log_name = "test_server"
    LogClient().init(log_name,rq_queue,rq_host,rq_port)
    print logger,type(logger)
    msg = "Now i send a msg to you spider"
    logger.info(msg)
    logger.debug(msg)
    logger.error(msg)
    LogClient().warn(msg)
    for i in range(0,1000000):
        LogClient().info("i send a msg to you")
    print "done"

