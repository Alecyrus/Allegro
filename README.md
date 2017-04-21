# Enigma
Enima is a python backend integration framework, which provides a simple way to make the task of building any kind of RESTFul system easy and efficient. The RESTFul service is based on [Sanix](https://github.com/channelcat/sanic), and [RabbitMQ](http://www.rabbitmq.com/) provides a message communication service. 

With the framework, the API can be defined through a config file, and we just focus on the processing logic. What's more, it' very efficient and easy for frond-end to build a mock server.

## Installation
> `pip3 install Engima`

It only supports Python3.5 or higher.

## Get Started
### main.py
```python
from enigma import Enigma
app = Enigma("test_project")
app.initialize("test.ini")
app.start()
```

### test.py
```python
from enigma.consumer import BaseConsumer

from pprint import pprint


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

```
### test.ini
```python
default]
;The ip address of the host you runs the RESTFul API service
bind_host = 0.0.0.0
;The port
bind_port = 8000
;The number of the RESTFul API service process
api_worker = 2
;The directory where the consumer modules you defined can be found 
consumer_path = /home/luze/Enigma/tests


[service]
;The services your projects provided. If you want to define more than
;one service, separate each service's name by a comma. And then you must 
;define every service's specific information with a section named after
;the service'name.
keys = Test1Service


[Test1Service]
;The uri of the service. And the api can be accessed by the url;
;(http://bind_host:bind_port/uri)
uri = /test1
;The message queue that the service uses
queue = test1
;The level of the parameter. If you set it with the integer 2, json and url request can be both accepted.
; 1 -> The json request(raw body) support.
; 2 -> The url  request(http://api/uri?param1=value1&param2=value2) support.
; 3 -> The form request(form body) support.
params = 3
;The handler class of the service's requests.
consumer = TestConsumer
;The module where the handler class is located
module = test
;The number of the handler process.
workers = 1

```
Run the command:
> `# python3 main.py`

If you send the request:
> `curl  -H "Accept: application/json" -d "Name=Alecyrus&Age=20" http://$iP:$port/test1`

you will get this respose:
>`{"info":"Your name is Alecyrus, and you are 20 years old.","state":1}`


## License
Enigma is open source and released under the MIT Licence.
