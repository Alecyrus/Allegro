class BaseConsumer(object):
    def __init__(self):
        super(BaseConsumer, self).__init__()
        self.failed_msg = "UNKOWN REQUEST"

    def _response(self, msg, success=False):
        response = {"state":0}
        if success:
            response["state"] = 1
        response["info"] = msg
        return response

    def get(self, message):
        return self._response(self.failed_msg)

    def post(self, message):
        return self._response(self.failed_msg)

    def update(self, message):
        return self._response(self.failed_msg)

    def delete(self, message):
        return self._response(self.failed_msg)

    def patch(self, message):
        return self._response(self.failed_msg)

    def put(self, message):
        return self._response(self.failed_msg)

