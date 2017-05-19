import time
import os

from pprint import pprint

from allegro.consumer import BaseConsumer
import time


class TestConsumer(BaseConsumer):
    def __init__(self):
        super(TestConsumer, self).__init__()

    def get(self, message):
        print("GET request received=============")
        pprint(message)
        print("=================================")
        return self._response("GET Received!!!", True)

    def post(self, message):
        print("POST request received============")
                 
        print(os.getpid())
        time.sleep(1)
        #resp = "Your name is %s, and you are %s years old." % (message['form_content']["Name"][0], message['form_content']["Age"][0])
        resp = "asdasdas"
        print("=================================")
        return self._response(resp, True)



