# src/task/tasks.py
import subprocess
import time
from .config import app  # config.py에서 app 객체를 가져옴
import sys
import os
from .parse.dataParse import hookCompareParse, minimumTestParse, getPriceUsingPyth, timeBasedMinimumTestParse
from .threadWork import threadRun
# 작업 정의
@app.task
def analysis(x, y):
    command = "sleep 20; ls; sleep 10; whoami"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
@app.task
def dynamic(timeHash, rpc, currency0, currency1):

    commands = []
    analysisResult = []
    # 목표 디렉토리 경로 설정 (상대 경로 사용)
    
    print("timeHash : {}".format(timeHash))
    print("rpc : {} , c0 : {} : c1 : {}".format(rpc,currency0, currency1))
    st = time.time()
    commands.append("forge test --match-path test/inputPoolkey/_MinimumTest.t.sol --rpc-url {}".format(rpc))
    commands.append("forge test --match-path test/inputPoolkey/_time_std_PoolManager.t.sol  --rpc-url {}".format(rpc))
    commands.append("forge test --match-path test/hookNoHookCompare/_hookNoHookCompare.t.sol --rpc-url {} -vv | grep using".format(rpc))
    commands.append("forge test --match-path test/inputPoolkey/_return.t.sol  --rpc-url {} -vv | grep delta-log".format(rpc))
    
    threads = []
    for command in commands:
        threads.append(threadRun(command))

    analysisResult = []
    for thread in threads:
        result = thread.join()
        analysisResult.append(result)
    ed = time.time()
    print("Done : {}".format(ed))
    print("time : {}".format(ed - st))
    print("start : {}".format(st))
    analysisResult[0] = minimumTestParse(analysisResult[0])
    print("end 0 ")
    analysisResult[1] = timeBasedMinimumTestParse(analysisResult[1])
    print("end 1")
    analysisResult[2] = hookCompareParse(analysisResult[2])
    print("end 2")
    analysisResult[3] = getPriceUsingPyth(rpc, currency0, currency1, analysisResult[3])#analysisResult[0]))
    ed = time.time()
    print("Done : {}".format(ed))
    print("time : {}".format(ed - st))
    print("start : {}".format(st))
    print(analysisResult)
    return analysisResult
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