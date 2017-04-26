#!/usr/bin/env python
# coding=utf-8

import sys,os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'submodules'))

import logging
import json
import ConfigParser
from Common.queues.rb_consumer import RQConsumer,TestConsumer

class LogServer(RQConsumer):
    
    def __init__(self,rq_queue,rq_host="127.0.0.1",rq_port=5672,kwags={}):
        self.loggers = {}
        RQConsumer.__init__(self,rq_queue,rq_host,rq_port,kwags)

    """
        处理从队列中取回的消息，并存放在对应的handler指向的文件中
        data = {
            "log_name":"spider_server",     #每个server对应一个log_name
            "msg":"send the msg",           #日志消息
            "level":"info/error/debug/warn",#日志级别                     
        }
        继承只RQConsumer
    """
    def data_process(self,data):
        try:
            j_data = json.loads(data)
            log_name = j_data["log_name"]
            if log_name not in self.loggers:
                new_log_name = self.get_handler(log_name)
                self.loggers[log_name] = new_log_name
            self.write(j_data)
        except Exception,e:
            print "LogServer data_process occure a Exception:{}".format(e)
            return

    def write(self,data):
        logger = self.loggers[data["log_name"]]
        if data["level"] == "info":
            logger.info(data["msg"])
        if data["level"] == "error":
            logger.error(data["msg"])
        if data["level"] == "debug":
            logger.debug(data["msg"])
        if data["level"] == "warn":
            logger.warn(data["msg"])

    def get_handler(self,log_name):
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("logs/{}.log".format(log_name))
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

if __name__ == "__main__":
    conf = ConfigParser.ConfigParser()
    conf.read("setting.conf")
    rq_host = conf.get("rabbitmq","host")
    rq_port = conf.get("rabbitmq","port")
    rq_queue = conf.get("rabbitmq","queue")
    TestConsumer(LogServer,rq_queue,rq_host,rq_port,{})

