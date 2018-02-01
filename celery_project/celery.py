from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('celery_project',broker='amqp://celery:celery@172.25.0.10/',backend='amqp://celery:celery@172.25.0.10/',include=['celery_project.tasks'])

if __name__ == '__main__':
    app.start()