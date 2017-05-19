from sanic.views import HTTPMethodView
from sanic.response import text
from sanic.response import json
from pprint import pprint


class BaseView(HTTPMethodView):
  def __init__(self, queue, rpc_client, params):
      self.queue = queue
      self.rpc_client = rpc_client
      self.params = params

  def request_to_message(self, request, optype):
      message = dict()
      message["optype"] = optype
      if self.params > 0:
          try:
              message["json_content"] = request.json
          except Exception:
              pass
      if self.params > 1:
          message["url_content"] = request.args
      if self.params > 2:
          message["form_content"] = request.form
      return message

  async def get(self, request):
      response = self.rpc_client.call(self.request_to_message(request, "GET"), self.queue)
      return json(eval(str(response)))

  async def post(self, request):

      response = self.rpc_client.call(self.request_to_message(request, "POST"), self.queue)
      return json(eval(str(response)))

  async def put(self, request):
      response = self.rpc_client.call(self.request_to_message(request, "PUT"), self.queue)
      return json(eval(str(response)))

  async def patch(self, request):
      response = self.rpc_client.call(self.request_to_message(request, "PATCH"), self.queue)
      return json(eval(str(response)))

  async def delete(self, request):
      response = self.rpc_client.call(self.request_to_message(request, "DELETE"), self.queue)
      return json(eval(str(response)))
