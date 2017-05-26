import time
import imp
import asyncio

from sanic.views import HTTPMethodView
from sanic.response import text
from sanic.response import json
from sanic.exceptions import ServerError

class BaseView(HTTPMethodView):
  def __init__(self, method, module, path, timeout):
      self.method = method
      try: 
          file, pathname, desc = imp.find_module(module,[path])
          self.moduleobj = imp.load_module(module, file, pathname, desc)
      except Exception as e:
          raise

  def request_to_message(self, request):
      message = dict()
      try:
          message["url_content"] = request.args
          message["form_content"] = request.form
          message["json_content"] = request.json
      except Exception:
          pass
      return message

  def return_check(self, response):
      if isinstance(response, dict):
          return json(response)
      else:
          raise ServerError("The `dict` is expected. Please check the type of the callback", status_code=401)


  async def get(self, request):
      if 'get' not in self.method:
          return ServerError("Not support", status_code=400)
      message = self.request_to_message(request)
      handler = "self.moduleobj.get.delay"
      callback = eval(handler)(message)
      while(not callback.ready()):
          await asyncio.sleep(1)      
      response = callback.result
      return self.return_check(response)

  async def post(self, request):
      if 'post' not in self.method:
          return ServerError("Not support", status_code=400)
      message = self.request_to_message(request)
      handler = "self.moduleobj.post.delay"
      callback = eval(handler)(message)
      while(not callback.ready()):
          await asyncio.sleep(1)      
      response = callback.result
      return self.return_check(response)

  async def put(self, request):
      if 'put' not in self.method:
          return ServerError("Not support", status_code=400)
      message = self.request_to_message(request)
      handler = "self.moduleobj.put.delay"
      callback = eval(handler)(message)
      while(not callback.ready()):
          await asyncio.sleep(1)      
      response = callback.result
      return self.return_check(response)

  async def patch(self, request):
      if 'patch' not in self.method:
          return ServerError("Not support", status_code=400)
      message = self.request_to_message(request)
      handler = "self.moduleobj.patch.delay"
      callback = eval(handler)(message)
      while(not callback.ready()):
          await asyncio.sleep(1)      
      response = callback.result
      return self.return_check(response)
  
  async def delete(self, request):
      if 'delete' not in self.method:
          return ServerError("Not support", status_code=400)
      message = self.request_to_message(request)
      handler = "self.moduleobj.delete.delay"
      callback = eval(handler)(message)
      while(not callback.ready()):
          await asyncio.sleep(1)      
      response = callback.result
      return self.return_check(response)
