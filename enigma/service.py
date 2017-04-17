from pprint import pprint

import core.rpc as rpc
import configparser

from consumers.test import TestConsumer

INI_PATH = "/home/luze/Enigma/enigma/config/enigma-server.ini"
CONTENT = ["json_content", "form_content", "url_content"]

class BaseService(rpc.RpcServer):
    def __init__(self, queue, consumer):
        super(BaseService, self).__init__()

        self.queue = queue
        self._init_rpc("localhost", self.queue)
        self.consumer = consumer


    def handler_request(self, message):
        """handle a specific request from amqp::templates
        """
        body = dict()
        optype = message.pop("optype")
        consumer = eval(self.consumer)()
        for content in message.keys():
            if message[content] != {} and message[content] != None:
                body[content] = message[content]
        pprint(body)
        return self._request_handler(consumer, optype, body)


def main():
    cf = configparser.ConfigParser()
    cf.read(INI_PATH)
    services = cf.get("service", "keys").split(',')
    for service in services:
        processList = []
        workers = cf.getint(service, "workers")
        consumer = cf.get(service, "consumer")
        queue = cf.get(service, "queue")
        for i in range(workers) :
            p = BaseService(queue, consumer)
            processList.append(p)
            p.start()
        for p in processList:
            with open("pid/process.pid", "a") as f:
                f.write(str(p.pid)+"\n")

if __name__ == "__main__":
    main()

