# src/task/config.py

from celery import Celery

app = Celery('task', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')
app.autodiscover_tasks(['task'])
