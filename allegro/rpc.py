# -*- coding: UTF-8 -*-

import pika
import types
import uuid
import time
from pprint import pprint
import json
import configparser
import uuid

from multiprocessing import Process

#INI_PATH = "/home/luze/Enigma/enigma/config/enigma-server.ini"

HOST = "localhost"
EXCHANGE = "allegro::%s" % str(uuid.uuid1()).replace("-","")[:10]
PREFETCH = 1


class RpcClient(object):
    def __init__(self, timeout):
        self.timeout = timeout
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=HOST, heartbeat_interval=0))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.exchange_declare(exchange=EXCHANGE,type='direct')
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


    def call(self, message, queue):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange=EXCHANGE,
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
                self.response = str({'info':'time out', 'state':0})
        return self.response



class RpcServer(Process):
    def __init__(self):
        super(RpcServer, self).__init__()


    def _init_rpc(self, amqp, queue):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=amqp))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=EXCHANGE, type='direct')

        self.channel.basic_qos(prefetch_count=PREFETCH)
        result = self.channel.queue_declare(queue=queue, durable=False)
        self.channel.queue_bind(exchange=EXCHANGE,
                                queue=result.method.queue,
                                routing_key=queue)
        self.channel.basic_consume(self._on_request, queue=queue, no_ack=False)


    def _on_request(self, ch, method, props, body):
        message = eval(body)

        response = self.handler_request(message)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def handler_request(self, message):

        return

    def _request_handler(self, conn, type, message):
        if type == "GET" :
            print("GET")
            return conn.get(message)
        elif type == "POST":
            print("POST")
            return conn.post(message)
        elif type == "UPDATE":
            return conn.update(message)
        elif type == "DELETE":
            return conn.delete(message)
        elif type == "PATCH":
            return conn.patch(message)
        elif type == "PUT":
            return conn.put(message)
        else:
            reponse = "Error: the optype is not valid."
            return reponse


    def run(self):
        self.channel.start_consuming()
                                                        
