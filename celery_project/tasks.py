from __future__ import absolute_import, unicode_literals
from celery_project.celery import app
import random
@app.task
def add():
    return 'fuck'

@app.task
def mul():
    a={}
    a['status'] = 'ok'
    a['result'] = 2
    return a