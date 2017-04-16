# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import pika
import types
import uuid
import time
from pprint import pprint
import json
import configparser


INI_PATH = "enigma-server.ini"

class RpcClient(object):
    def __init__(self):
        self.init_param()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host, heartbeat_interval=0))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.exchange_declare(exchange=exchange,type='direct')
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)
    def init_param(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(INI_PATH)
        self.host = self.cf.get("rpc", "rpc_host")
        self.timeout = self.cf.getfloat("rpc", "timeour")
        self.exchange = self.cf.get("rpc", "exchange")



    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


    def call(self, message, queue):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=queue,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(message))
        start = time.time()
        while self.response is None:
            self.connection.process_data_events()
            if time.time()-start > self.timeout: #if timeout raise error
                self.response = {'timeout':time.clock()}
        return self.response
