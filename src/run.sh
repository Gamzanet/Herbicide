service redis-server start
service rabbitmq-server start
cd src
uvicorn run:app --host 0.0.0.0 --port 8000