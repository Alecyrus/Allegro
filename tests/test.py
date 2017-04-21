import time

from pprint import pprint

from enigma.consumer import BaseConsumer



class TestConsumer(BaseConsumer):
    def __init__(self):
        super(TestConsumer, self).__init__()

    def get(self, message):
        print("======================")
        pprint(message)
        print("======================")
        return self._response("GET Received!!!", True)

    def post(self, message):
        print("==========POST======")
        pprint(message)
        print("======================")
        print("======================")
        return self._response("POST Received!!!", True)



