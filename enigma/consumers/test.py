import time

from pprint import pprint

from core.consumer import BaseConsumer



class TestConsumer(BaseConsumer):
    def __init__(self):
        super(TestConsumer, self).__init__()

    def get(self, message):
        print("======================")
        pprint(message)
        print("======================")
        return self._response("Received!!!", True)




