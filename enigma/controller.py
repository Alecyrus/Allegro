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
      #print(type(request.form))
      #pprint(request.form)
      message = dict()
      message["optype"] = optype
      print(self.params)
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
      return json({"message":"get %s" %(str(self.queue), param)})

  async def post(self, request):
      message = self.request_to_message(request, "POST")
      #response = await self.rpc_client.call(self.request_to_message(request, "POST"), self.queue)
      #pprint(response)
      pprint(message)
      return json({"message":"post %s" %str(self.queue)})

  async def put(self, request):
      message = self.request_to_message(request, "POST")
      #response = await self.rpc_client.call(self.request_to_message(request, "POST"), self.queue)
      pprint(message)

      return json({"message":"put %s" %str(self.queue)})

  async def patch(self, request):
      message = self.request_to_message(request, "POST")
      #response = await self.rpc_client.call(self.request_to_message(request, "POST"), self.queue)
      pprint(message)
      return json({"message":"patch %s " %str(self.queue)})

  async def delete(self, request):
      message = self.request_to_message(request, "POST")
      #response = await self.rpc_client.call(self.request_to_message(request, "POST"), self.queue)
      pprint(message)
      return json({"message":"delete %s " %str(self.queue)})
