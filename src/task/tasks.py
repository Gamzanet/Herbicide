# src/task/tasks.py
import subprocess
import time
from .config import app  # config.py에서 app 객체를 가져옴
import sys
import os
from .parse.dataParse import hookCompareParse, minimumTestParse, getPriceUsingPyth, timeBasedMinimumTestParse, getChkOnlyByPoolManager, timeTestUsingStep
from .staticRun import staticRun
from .threadWork import threadRun
# 작업 정의
@app.task
def analysis(x, y):
    command = "sleep 20; ls; sleep 10; whoami"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
@app.task
def dynamic(timeHash, rpc, currency0, currency1, hooks):
 
    commands = []
    analysisResult = []
    # 목표 디렉토리 경로 설정 (상대 경로 사용)
    
    print("timeHash : {}".format(timeHash))
    print("rpc : {} , c0 : {} : c1 : {}".format(rpc,currency0, currency1))
    st = time.time()
    option = "--rpc-url {}".format(rpc)
    _exportPath = "export _targetPoolKey='dynamic_{}_{}.json';".format(timeHash,hooks)
    #head = "forge test --match-path test/inputPoolkey/"
    #tests = ["_MinimumTest.t.sol","_time_std_PoolManager.t.sol","_hookNoHookCompare.t.sol -vv | grep using","_return.t.sol","_check_onlyByPoolManager.t.sol"]
    #for _test in tests:
    #    commands.append("{}{} {}".format(head,_test, option))
    # commands.append("forge test --match-path test/inputPoolkey/  --rpc-url {}".format(rpc))
    # commands.append("forge test --match-path test/inputPoolkey/  --rpc-url {}".format(rpc))
    # commands.append("forge test --match-path test/inputPoolkey/ --rpc-url {} ".format(rpc))
    # commands.append("forge test --match-path test/inputPoolkey/  --rpc-url {} -vv | grep delta-log".format(rpc))
    # asd = subprocess.run("anvil --rpc-url https://unichain-sepolia.g.alchemy.com/v2/LVjDyU_Hfup9CLkn7lAl6LYu8cCw4HJm", shell=True, capture_output=True, text=True)

    commands.append("{} forge test --match-path test/inputPoolkey/_MinimumTest.t.sol --rpc-url {} -vvv".format(_exportPath,rpc))
    commands.append("{} forge test --match-path test/inputPoolkey/_time_std_PoolManager.t.sol  --rpc-url {} -vvv".format(_exportPath,rpc))
    commands.append('{} forge test --match-path test/inputPoolkey/_hookNoHookCompare.t.sol --rpc-url {} -vv | grep using'.format(_exportPath,rpc))
    commands.append('{} forge test --match-path test/inputPoolkey/_return.t.sol  --rpc-url {} -vv | grep -Ei "Amount[0-1]+ delta:"'.format(_exportPath,rpc))
    commands.append("{} forge test --match-path test/inputPoolkey/_check_onlyByPoolManager.t.sol --rpc-url {}".format(_exportPath,rpc))
    commands.append("{} forge test --match-path test/inputPoolkey/_time_minimum_step.t.sol --rpc-url {} -vvv".format(_exportPath,rpc))

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
    analysisResult[4] = getChkOnlyByPoolManager(analysisResult[4])
    analysisResult[5] = timeTestUsingStep(analysisResult[5])

    ed = time.time()
    print("Done : {}".format(ed))
    print("time : {}".format(ed - st))
    print("start : {}".format(st))
    print(analysisResult)
    response = {}
    response["analysisResult"] = analysisResult
    response["hooks"] = hooks
    return analysisResult

@app.task
def static(timeHash, hook):
    
    tmp = staticRun(timeHash, hook)
    
    return tmp