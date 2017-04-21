from sanic import Sanic
from sanic.response import json
from sanic.response import text

import os
import configparser

from .controller import BaseView
from .rpc import RpcClient
import logging


from .service import BaseService

class Enigma(object):
    def __init__(self, name):
        self.log = logging.getLogger('enigma')


        formatter = logging.Formatter(
                    "%(asctime)s: %(levelname)s: %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.INFO)

        self.app = Sanic(name)
        self.pid_path = "/tmp/%s" % name
        open(self.pid_path,"w+").close()

    
    def initialize(self, config_path):
         
        try:
            self.cf = configparser.ConfigParser()
            self.cf.read(config_path)
         
            # SERVER
            self.host = self.cf.get("default", "bind_host")
            self.port = self.cf.getint("default", "bind_port")
            self.wokers = self.cf.getint("default", "api_worker")
            self.consumer_path = self.cf.get("default", "consumer_path")

        except Exception as e:
            self.log.exception("Error ocurred when trying to the config file Info: %s" % str(e))
            raise

    def init_route(self):
        services = self.cf.get("service", "keys").split(',')
        for service in services:
            rpc_client = RpcClient()
            queue = self.cf.get(service, "queue") 
            uri = self.cf.get(service, "uri")
            params =  self.cf.getint(service, "params")
            self.app.add_route(BaseView.as_view(queue, rpc_client, params), uri)

    def start(self):
        try:
            self.init_route()
            with open(self.pid_path, "a") as f:
                f.write(str(os.getpid())+"\n")

            #self.app.run(host=self.host, port=self.port, workers=self.wokers)
            self.log.info("Starting Consumer service...")
            services = self.cf.get("service", "keys").split(',')
            for service in services:
                processList = []
                workers = self.cf.getint(service, "workers")
                consumer = self.cf.get(service, "consumer")
                queue = self.cf.get(service, "queue")
                module = self.cf.get(service, "module")
                for i in range(workers) :
                    try:
                        p = BaseService(queue, consumer, module, self.consumer_path)
                    except Exception as e:
                        self.log.exception("Failed to import %s module from %s" % (self.consumer))
                        raise
                    processList.append(p)
                    p.start()
                for p in processList:
                    with open(self.pid_path, "a") as f:
                        f.write(str(p.pid)+"\n")
            #self.init_route()
            #with open(self.pid_path, "a") as f:
            #    f.write(str(os.getpid())+"\n")
            self.log.info("Starting API service...")

            self.app.run(host=self.host, port=self.port, workers=self.wokers)


        except Exception as e:
            self.log.exception("Error ocurred when trying to the config file Info: %s" % str(e))
            raise

    def stop(self):
        try:
            self.app.stop()
            with open(self.pid_path, "r") as f:
                processes = f.readlines()
                for p in processes:
                    os.kill(pid, signal.SIGKILL)
            open(self.pid_path, "w+")
        except Exception as e:
            log.exception("Error ocurred when trying to kill the processes Info: %s" % str(e)) 
            raise

