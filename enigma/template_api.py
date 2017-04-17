# Copyright (c) 2016 NIST
# All Rights Reserved.
# Author: Junkai Huang

#!/usr/bin/env python

import os
import sys

import pika
import logging
from pprint import pprint

import common.rpc as rpc
from common import cloghandler
from flavor import FlavorsManager
from image  import ImagesManager

URL = "amqp://guest:hitnslab@172.29.152.246:5672/"
LOG =  logging.getLogger("template")

class TemplateService(rpc.base_RPC):
    def __init__(self):
        super(TemplateService, self).__init__()

        url = URL
        queue = ["springx::template::flavor", "springx::template::image"]

        self._init_rpc("localhost", queue)


    def handler_request(self, message):
        """handle a specific request from amqp::templates
        """
        optype = message['optype']
        cmdtype = message['cmdtype']
        body = message['content']
        if optype == "flavor":
                fla = FlavorsManager()
                return self._request_handler(fla, cmdtype, body)
        elif optype == "image":
                ima = ImagesManager()
                return self._request_handler(ima, cmdtype, body)
        else:
                LOG.error("otype is NOT vaild, More info%s" %str(message))
                return False

def main():
    processList = []
    for i in range(4) :
        p = TemplateService()
        processList.append(p)
        p.start()

    for p in processList:
        with open("pid/process.pid", "a") as f:
            f.write(str(p.pid)+"\n")

if __name__ == "__main__":
    main()

