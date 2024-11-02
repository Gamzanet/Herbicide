# src/task/tasks.py
import subprocess
import time
from .config import app  # config.py에서 app 객체를 가져옴
import sys
import os
from .parse.dataParse import hookCompareParse, minimumTestParse, getPriceUsingPyth, timeBasedMinimumTestParse, getChkOnlyByPoolManager, timeTestUsingStep, doubleInitParse, upgradableParse
from .staticRun import staticRun, staticRunByCode
from .threadWork import threadRun, testRun
# 작업 정의
@app.task
def analysis(x, y):
    command = "sleep 20; ls; sleep 10; whoami"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
@app.task
def dynamic(timeHash, rpc, poolkey):
    commands = []
    analysisResult = []
    # 목표 디렉토리 경로 설정 (상대 경로 사용)
    
    print("timeHash : {}".format(timeHash))
    print("rpc : {} , c0 : {} : c1 : {}".format(rpc,poolkey["currency0"], poolkey["currency1"]))
    st = time.time()
    option = "--rpc-url {}".format(rpc)
    _exportPath = "export _targetPoolKey='dynamic_{}_{}.json';".format(timeHash, poolkey["hooks"])

    commands.append("{} forge test --match-path test/inputPoolkey/MinimumTest.t.sol --rpc-url {} -vvv".format(_exportPath,rpc))
    commands.append("{} forge test --match-path test/inputPoolkey/time_std_PoolManager.t.sol  --rpc-url {} -vvv".format(_exportPath,rpc))
    commands.append('{} forge test --match-path test/inputPoolkey/hookNoHookCompare.t.sol --rpc-url {} -vv | grep using'.format(_exportPath,rpc))
    commands.append('{} forge test --match-path test/inputPoolkey/return.t.sol  --rpc-url {} -vv | grep -Ei "Amount[0-1]+ delta:"'.format(_exportPath,rpc))
    commands.append("{} forge test --match-path test/inputPoolkey/check_onlyByPoolManager.t.sol --rpc-url {}".format(_exportPath,rpc))
    commands.append("{} forge test --match-path test/inputPoolkey/time_minimum_step.t.sol --rpc-url {} -vvv".format(_exportPath,rpc))
    commands.append("{} forge test --match-path test/inputPoolkey/check_doubleInit.t.sol --rpc-url {}".format(_exportPath,rpc))
    commands.append("{} forge test --match-path test/inputPoolkey/check_upgradable.t.sol --rpc-url {}".format(_exportPath,rpc))
    
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
    analysisResult[3] = getPriceUsingPyth(rpc, poolkey["currency0"], poolkey["currency1"], analysisResult[3])#analysisResult[0]))
    analysisResult[4] = getChkOnlyByPoolManager(analysisResult[4])
    analysisResult[5] = timeTestUsingStep(analysisResult[5])

    analysisResult[6] = doubleInitParse(analysisResult[6])
    analysisResult[7] = upgradableParse(analysisResult[7])

    ed = time.time()
    print("Done : {}".format(ed))
    print("time : {}".format(ed - st))
    print("start : {}".format(st))
    print(analysisResult)
    
    
    response = {}
    response["analysisResult"] = analysisResult
    
    response["poolKey"] = poolkey
    response["mode"] = 2
    return response

@app.task
def dynamic_minimum(timeHash, rpc, poolkey, idx):
    response = {}
    st = time.time()
    _exportPath = "export _targetPoolKey='dynamic_{}_{}.json';".format(timeHash, poolkey["hooks"])
    cmd = "{} forge test --match-path test/inputPoolkey/MinimumTest.t.sol --fork-url {} -vvv".format(_exportPath,rpc)

    res = minimumTestParse(testRun(cmd))
    response["timeHash"] = timeHash
    response["poolKey"] = poolkey
    response["mode"] = 2
    response["result"] = res
    response["idx"] = idx
    ed = time.time()
    response["time"] = ed - st

    return response

@app.task
def dynamic_timeBasedMinimumTest(timeHash, rpc, poolkey, idx):
    response = {}
    st = time.time()
    _exportPath = "export _targetPoolKey='dynamic_{}_{}.json';".format(timeHash, poolkey["hooks"])
    cmd = "{} forge test --match-path test/inputPoolkey/time_std_PoolManager.t.sol  --fork-url {} -vvv".format(_exportPath,rpc)
    res = timeBasedMinimumTestParse(testRun(cmd))
    response["timeHash"] = timeHash
    response["poolKey"] = poolkey
    response["mode"] = 2
    response["result"] = res
    response["idx"] = idx
    ed = time.time()
    response["time"] = ed - st
    return response

@app.task
def dynamic_hookCompare(timeHash, rpc, poolkey, idx):
    response = {}
    st = time.time()
    _exportPath = "export _targetPoolKey='dynamic_{}_{}.json';".format(timeHash, poolkey["hooks"])

    cmd = '{} forge test --match-path test/inputPoolkey/hookNoHookCompare.t.sol --fork-url {} -vv | grep using'.format(_exportPath,rpc)

    res = hookCompareParse(testRun(cmd))
    response["timeHash"] = timeHash
    response["poolKey"] = poolkey
    response["mode"] = 2
    response["result"] = res
    response["idx"] = idx
    ed = time.time()
    response["time"] = ed - st
    return response

@app.task
def dynamic_priceCheck(timeHash, rpc, poolkey, idx):
    response = {}
    st = time.time()
    _exportPath = "export _targetPoolKey='dynamic_{}_{}.json';".format(timeHash, poolkey["hooks"])
    cmd = '{} forge test --match-path test/inputPoolkey/returnDelta.t.sol --fork-url {} -vv | grep -Ei "Amount[0-1]+ delta:|-for-expected-current-|-for-expected-amount0"'.format(_exportPath,rpc)
    res = getPriceUsingPyth(rpc, poolkey["currency0"], poolkey["currency1"], testRun(cmd))
    response["timeHash"] = timeHash
    response["poolKey"] = poolkey
    response["mode"] = 2
    response["result"] = res
    response["idx"] = idx
    ed = time.time()   
    response["time"] = ed - st
    return response

@app.task
def dynamic_OnlyByPoolManager(timeHash, rpc, poolkey, idx):
    response = {}
    st = time.time()
    _exportPath = "export _targetPoolKey='dynamic_{}_{}.json';".format(timeHash, poolkey["hooks"])

    cmd = "{} forge test --match-path test/inputPoolkey/check_onlyByPoolManager.t.sol --fork-url {}".format(_exportPath,rpc)

    res = getChkOnlyByPoolManager(testRun(cmd))
    response["timeHash"] = timeHash
    response["poolKey"] = poolkey
    response["mode"] = 2
    response["result"] = res
    response["idx"] = idx
    ed = time.time()
    response["time"] = ed - st
    return response
@app.task
def dynamic_timeTestUsingStep(timeHash, rpc, poolkey, idx):
    response = {}
    st = time.time()
    _exportPath = "export _targetPoolKey='dynamic_{}_{}.json';".format(timeHash, poolkey["hooks"])

    cmd = "{} forge test --match-path test/inputPoolkey/time_minimum_step.t.sol --fork-url {} -vvv".format(_exportPath,rpc)

    res = timeTestUsingStep(testRun(cmd))
    response["timeHash"] = timeHash
    response["poolKey"] = poolkey
    response["mode"] = 2
    response["result"] = res
    response["idx"] = idx
    ed = time.time()
    response["time"] = ed - st
    return response
@app.task
def dynamic_doubleInit(timeHash, rpc, poolkey, idx):
    response = {}
    st = time.time()
    _exportPath = "export _targetPoolKey='dynamic_{}_{}.json';".format(timeHash, poolkey["hooks"])
    cmd = "{} forge test --match-path test/inputPoolkey/check_doubleInit.t.sol --fork-url {} -vv".format(_exportPath,rpc)
    res = doubleInitParse(testRun(cmd))
    response["timeHash"] = timeHash
    response["poolKey"] = poolkey
    response["mode"] = 2
    response["result"] = res
    response["idx"] = idx
    ed = time.time()
    response["time"] = ed - st
    return response
@app.task
def dynamic_upgradable(timeHash, rpc, poolkey, idx):
    response = {}
    st = time.time()
    _exportPath = "export _targetPoolKey='dynamic_{}_{}.json';".format(timeHash, poolkey["hooks"])
    cmd = "{} forge test --match-path test/inputPoolkey/check_upgradable.t.sol --fork-url {}".format(_exportPath,rpc)
    res = upgradableParse(testRun(cmd))
    response["timeHash"] = timeHash
    response["poolKey"] = poolkey
    response["mode"] = 2
    response["result"] = res
    response["idx"] = idx
    ed = time.time()
    response["time"] = ed - st
    return response

@app.task
def static(timeHash, poolKey):
    print("poolkey")
    print(poolKey)
    tmp = staticRun(timeHash, poolKey["hooks"])
    tmp["idx"] = 0
    tmp["poolKey"] = poolKey
    
    return tmp

@app.task
def static_by_code(timeHash,codeHash, src):

    print(src)
    tmp = staticRunByCode(timeHash, codeHash,src)
    tmp["idx"] = 0
    tmp["codeHash"] = codeHash
    
    return tmp