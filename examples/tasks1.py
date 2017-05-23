#!/usr/bin/env python
# coding=utf-8
from celery import Celery

from pprint import pprint
import time
app = Celery('tasks', backend='redis://localhost:6379/0', broker = 'redis://localhost:6379/0')


@app.task
def get(message):
    pprint(message)
    #time.sleep(4)
    return {"app":"Get Got"}

@app.task
def post(message):
    pprint(message)
    #time.sleep(4)
    #return {"app":"post Got"}
    return {"app":"Post Got"}

