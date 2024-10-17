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
def dynamic(rpc):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 목표 디렉토리 경로 설정 (상대 경로 사용)
    target_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'engine', 'gamza-dynamic'))
    
    command = "forge test --match-path test/_inputPoolkey_PoolManager.t.sol --rpc-url {}".format(rpc)
    print(subprocess.run("pwd",shell=True, text=True).stdout)
    print(command)
    path = os.path.abspath(__file__)
    print(path)
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=target_dir)
    return result.stdout.split("\n")
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