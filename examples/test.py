import time

from pprint import pprint

from enigma.consumer import BaseConsumer



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
        pprint(message)
        resp = "Your name is %s, and you are %s years old." % (message['form_content']["Name"][0], message['form_content']["Age"][0])
        print("=================================")
        return self._response(resp, True)



