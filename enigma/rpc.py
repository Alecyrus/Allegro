import os
import sys

import pika
from multiprocessing import Process
import cloghandler

from pprint import pprint


EXCHANGE_NAME="springx"


class RpcServer(Process):
        def __init__(self):
                super(RpcServer, self).__init__()


        def _init_rpc(self, amqp, queue):
                #parameters = pika.URLParameters(amqp)
                #parameters = pika.ConnectionParameters(host=amqp)
                #conn = pika.BlockingConnection(parameters)
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=amqp))
                self.channel = connection.channel()
                self.channel.exchange_declare(exchange=EXCHANGE_NAME, type='direct')
                self.channel.basic_qos(prefetch_count=1)

                for q in queue:
                        result =  self.channel.queue_declare(queue=q, durable=True)
                        self.channel.queue_bind(exchange=EXCHANGE_NAME,
                                                queue=result.method.queue,
                                                routing_key=q)
                        self.channel.basic_consume(self._on_request, queue=q, no_ack=False)



        def _on_request(self, ch, method, props, body):
                message = eval(body)
                pprint(message)

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
                        return conn.get(message)
                elif type == "POST":
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

