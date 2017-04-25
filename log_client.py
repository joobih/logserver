#!/usr/bin/env python
# coding=utf-8

import pika
from singleton import singleton

@singleton
class log_client(object):
    
    def __init__(self):
        pass

    def info(self,data):
        msg = {"log_name":self.log_name,"level":"info","data":data}
        self.handler.send(msg)
