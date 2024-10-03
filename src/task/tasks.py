# src/task/tasks.py
import subprocess
import time
from .config import app  # config.py에서 app 객체를 가져옴

# 작업 정의
@app.task
def analysis(x, y):
    command = "sleep 20; ls; sleep 10; whoami"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
@app.task
def dynamic(x):
    command = "sleep 30; whoami"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
@app.task
def static(id):
    command = "semgrep --config ~/semgrep/myRules ~/tmp/{}.sol".format(id)
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("run")
    print(result.stderr)
    print(result.stdout)
    return result.stdout