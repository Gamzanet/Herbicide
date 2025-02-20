#!/bin/bash

echo "🔄 Restarting FastAPI server and worker processes..."

# ✅ 1. 기존 FastAPI 및 Worker 프로세스 종료
echo "🛑 Stopping existing FastAPI server..."
pkill -f "uvicorn run:app"  # 실행 중인 Uvicorn 종료

echo "🛑 Stopping existing Worker..."
pkill -f "sh worker.sh"  # 실행 중인 worker.sh 종료

# 2초 대기 (안정적인 종료를 위해)
sleep 2

# ✅ 2. Redis & RabbitMQ 서버 실행 (이미 실행 중이라면 무시됨)
echo "🚀 Starting Redis & RabbitMQ servers..."
service redis-server start
service rabbitmq-server start

# ✅ 3. FastAPI 서버 실행
echo "🌍 Starting FastAPI server..."
nohup uvicorn run:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &

# ✅ 4. Worker 실행
echo "⚙️  Starting Worker process..."
nohup sh worker.sh > worker.log 2>&1 &

echo "✅ FastAPI server and worker restarted successfully!"