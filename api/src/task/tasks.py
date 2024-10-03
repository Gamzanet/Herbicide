# src/task/tasks.py
import subprocess
from .config import app  # config.py에서 app 객체를 가져옴

# 작업 정의
@app.task
def analysis(x, y):
    command = "ls"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
