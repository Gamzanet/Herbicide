#celery -A task.config worker --loglevel=info
celery -A task.config worker -l INFO -P threads -c 10
