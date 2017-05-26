import os
import configparser
import logging
import signal
import subprocess

from asyncio import get_event_loop
from sanic import Sanic
from sanic.response import json
from sanic.config import Config
from sanic.response import text


from .controller import BaseView

class Allegro(object):
    def __init__(self, name):
        self.log = logging.getLogger('allegro')

        formatter = logging.Formatter(
                    "%(asctime)s: %(levelname)s: %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.INFO)

        self.app = Sanic(name)
    
    def initialize(self, config_path):
         
        try:
            self.cf = configparser.ConfigParser()
            self.cf.read(config_path)
         
            self.host = self.cf["basic"]["bind_host"]
            self.port = int(self.cf["basic"]["bind_port"])
            self.root_path = self.cf["basic"]["root_path"]
            self.api_worker = int(self.cf["basic"]["api_worker"])
            self.pid_path = self.cf["basic"]["pid_path"]
            self.timeout = int(self.cf["basic"]["timeout"])
            self.app.config.REQUEST_TIMEOUT=self.timeout

        except Exception as e:
            self.log.exception("Error ocurred when trying to the config file Info: %s" % str(e))
            raise

    def init_route(self):
        services = self.cf["service"]["keys"].replace(' ', '').split(',')
        for service in services:
            uri = self.cf[service]["uri"]
            module = self.cf[service]["module"]
            method = self.cf[service]["method"].lower().replace(' ','').split(',')
            self.app.add_route(BaseView.as_view(method, module, self.root_path, self.timeout), uri)

    def start(self):
        try:
            self.init_route()
            with open(self.pid_path, "a") as f:
                f.write(str(os.getpid())+"\n")

            services = self.cf["service"]["keys"].split(',')
            os.system('cd %s' % self.root_path)
            for service in services:
                module = self.cf[service]["module"]
                eventlet_enabled = eval(self.cf[service]['eventlet_enabled'])
                if eventlet_enabled:
                    eventlet_pool = int(self.cf[service]["eventlet_pool"])
                    subprocess.call('celery worker -A %s --concurrency 1   -l info -P eventlet -c %s -n %s &' % (module, eventlet_pool, module), shell=True)
                else:
                    workers = int(self.cf[service]["workers"])
                    for i in range(workers):
                        subprocess.call('celery worker -A %s --concurrency %s   -l info -n %s%s &' % (module, workers, module, i), shell=True)

            self.log.info("Starting Consumer service...")
            self.app.add_task(self.save_pid())
            self.app.run(host=self.host, port=self.port, workers=self.api_worker)
        except Exception as e:
            self.log.exception("Error ocurred when trying to the config file Info: %s" % str(e))
            raise

    async def save_pid(self):
        with open(self.pid_path, "a") as f:
            f.write(str(os.getpid())+"\n")

    def stop(self):
        try:
            self.log.info("Staring to termina the processes...")
            with open(self.pid_path, "r") as f:
                processes = f.readlines()
                for p in processes:
                    try:
                        a = os.kill(int(p[:-1]), signal.SIGKILL)
                    except Exception as e:
                        self.log.error(e)
            open(self.pid_path, "w+")
            os.system("pkill -9 -f 'celery worker'")
            self.log.info("All the processes are terminated.")
        except Exception as e:
            log.exception("Error ocurred when trying to kill the processes Info: %s" % str(e)) 
            raise

