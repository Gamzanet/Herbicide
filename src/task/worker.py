# src/task/worker.py

from .config import app

if __name__ == '__main__':
    # Celery 워커 실행
    app.start()
