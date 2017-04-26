#!/usr/bin/env python
# coding=utf-8

import sys,os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'submodules'))

import ConfigParser
from Common.queues.rb_product import RQProduct
#from singleton import singleton

class LogClient(object):
    __instance = None    

    def __new__(cls,*args,**kwd):
        print "__new__"
        if LogClient.__instance is None:
            LogClient.__instance=object.__new__(cls,*args,**kwd)
        return LogClient.__instance

    def __init__(self,log_name,rq_queue,rq_host="127.0.0.1",rq_port=5672):
        print "__init__",log_name
        self.log_name = log_name
        self.product = RQProduct(rq_queue,rq_host,rq_port)

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
    logger = LogClient(log_name,rq_queue,rq_host,rq_port)
    print logger,type(logger)
    msg = "Now i send a msg to you"
    logger.info(msg)
    logger.debug(msg)
    logger.error(msg)
    logger.warn(msg)
    log_name = "spider_server"
    logger = LogClient(log_name,rq_queue,rq_host,rq_port)
    print logger,type(logger)
    msg = "Now i send a msg to you spider"
    logger.info(msg)
    logger.debug(msg)
    logger.error(msg)
    logger.warn(msg)
