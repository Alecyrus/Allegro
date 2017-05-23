import time
import os

from pprint import pprint

from allegro.consumer import BaseConsumer
import time
import asyncio


class TestConsumer(BaseConsumer):
    def __init__(self):
        super(TestConsumer, self).__init__()

    def get(self, message):
        print("GET request received=============")
        pprint(message)
        print("=================================")

    def post(self, message):
        print("POST request received============")
                 
        print(os.getpid())
        #print ("Starting")
        time.sleep(5)
        #print ("End")
        #resp = "Your name is %s, and you are %s years old." % (message['form_content']["Name"][0], message['form_content']["Age"][0])
        resp = "Post Got"
        print("=================================")
        return self._response(resp, True)



