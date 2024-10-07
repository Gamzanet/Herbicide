# src/task/tasks.py
import subprocess
import time
from .config import app  # config.py에서 app 객체를 가져옴
import sys
import os

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
    src = os.path.dirname(os.path.abspath(__file__))
    engine_path = os.path.join(src, '..', '..', 'engine', 'gamza-static')
    sys.path.append(engine_path)
    import main
    res = main.is_valid_hook(_target_path="~/tmp/static_{}.sol".format(id))
    print("asdfasas : ~/tmp/static_{}.sol".format(id))
    print("===res===")
    print(res)

    command = "semgrep --config ~/semgrep/myRules ~/tmp/static_{}.sol --emacs".format(id)
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("run")
    tmp = {
        "res" : res,
        "result" : result.stdout
    }
    print(result.stderr)
    print(result.stdout)
    return tmp