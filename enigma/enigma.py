from sanic import Sanic
from sanic.response import json
from sanic.response import text


import configparser
from controller import BaseView
from rpc_client import RpcClient

app = Sanic(__name__)
INI_PATH = "enigma-server.ini"

class Engine(object):
    def __init__(self):
        self.init_param()
    
    def init_param(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(INI_PATH)
        
        # SERVER
        self.host = self.cf.get("default", "bind_host")
        self.port = self.cf.getint("default", "bind_port")
        self.wokers = self.cf.getint("default", "api_worker")

    @app.middleware('request')
    async def halt_request(request):
        print("before")

    @app.middleware('response')
    async def halt_response(request, response):
        print("after")

    def init_route(self, app):
        services = self.cf.get("service", "keys").split(',')
        #print(type(services)) 
        #print(len(services)) 
        for service in services:
            rpc_client = RpcClient()
            queue = self.cf.get(service, "queue") 
            uri = self.cf.get(service, "uri")
            params =  self.cf.getint(service, "params")
            app.add_route(BaseView.as_view(queue, rpc_client, params), uri)

    def start(self, app):
        self.init_route(app)
        app.run(host=self.host, port=self.port, workers=self.wokers)


if __name__ == "__main__":
    engine = Engine()
    engine.start(app)
