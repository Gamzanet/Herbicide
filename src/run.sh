service redis-server start
service rabbitmq-server start
nohup uvicorn run:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
nohup sh worker.sh > worker.log 2>&1 &
