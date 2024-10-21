import os
import sys
import re

def hookCompareParse(result):
    result = result.stdout.split("\n")
    ret = {}
    ret["name"] = "hook-NoHook-Compare"
    for i in range(len(result)-1):
        tmp = result[i].split(" :  ")
        ret[tmp[0].replace(" ","").replace("-using", "")] = tmp[1].replace(" ","")
    return ret

def foundryTestParse(result):
    realRet = {}
    result = result.stdout.split("Suite result:")[0]
    ret = []
    p = 0
    f = 0
    passed = re.findall(r'^\[PASS\].*', result, re.MULTILINE)
    failed = re.findall(r'^\[FAIL:.*', result, re.MULTILINE)
    
    tmp = passed + failed
    for i in range(len(tmp)):
        retTmp = {}
        if("[PASS" in tmp[i]): #[PASS
            retTmp["status"] = "PASS"
            retTmp["statusCode"] = 1
            p += 1
        if("[FAIL:" in tmp[i]):
            retTmp["status"] = "FAIL"
            retTmp["statusCode"] = 0
            f += 1
        retTmp["name"] = tmp[i].split("] ")[1].split(" ")[0]
        retTmp["msg"] = tmp[i]
        ret.append(retTmp)
    realRet["testList"] = ret
    realRet["PASS"] = p
    realRet["FAIL"] = f
    return realRet

def minimumTestParse(result):
    traces = re.findall(r'Traces:\n(.*?)(?=\n\n|\Z)', result.stdout, re.DOTALL)
    realRet = foundryTestParse(result)
    realRet["name"] = "Minimum_Test"
    msgs = [
        "Fail to add liquidity",
        "Fail to add liquidity twice within same range",
        "Fail to add liquidity through ERC6909",
        "Fail to remove liquidity",
        "Fail to remove partial liquidity",
        "Fail to receive ERC6909 with remove liquidity",
        "Fail to swap",
        "Fail to swap with highly pricelimit delta",
        "Fail to swap, using takeClaims",
        "Fail to swap, using takeClaims",
        "Fail to swap, using settleUsingBurn",
        "Fail to check protocolFee works well",
        "Fail to donate, when Pool has liquidity",
        "Fail to donate with one Token",
        "Fail to check emit log, when donate to pool",
        "test_collectProtocolFees_ERC20_accumulateFees_gas",
        "test_collectProtocolFees_ERC20_accumulateFees_exactOutput",
        "test_collectProtocolFees_ERC20_returnsAllFeesIf0IsProvidedAsParameter"
    ]
    failCnt = 0
    for i in range(len(realRet["testList"])):
        if(realRet["testList"][i]["status"] == "FAIL"):
            try:
                realRet["testList"][i]["description"] = msgs[i]
                realRet["testList"][i]["trace"] = traces[failCnt]
                if( "[OutOfGas] EvmError: OutOfGas" in traces[failCnt] ):
                    realRet["testList"][i]["OOG"] = 1
                else:
                    realRet["testList"][i]["OOG"] = 0
                

                failCnt += 1
            except:
                realRet["testList"][i]["description"] = "msg"                
                realRet["testList"][i]["trace"] = "trace not found"          
    return realRet

def timeBasedMinimumTestParse(result):
    traces = re.findall(r'Traces:\n(.*?)(?=\n\n|\Z)', result.stdout, re.DOTALL)
    realRet = foundryTestParse(result)
    realRet["name"] = "Time-Based-Minimum_Test"

    failCnt = 0
    for i in range(len(realRet["testList"])):
        if(realRet["testList"][i]["status"] == "FAIL"):
            try:
                realRet["testList"][i]["trace"] = traces[failCnt]
                failCnt += 1
            except:            
                realRet["testList"][i]["trace"] = "trace not found"      
    return realRet

def getPriceUsingPyth(rpc_url, token0_address, token1_address, result): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    engine_path = os.path.join(current_dir,'..','..', '..', 'engine', 'gamza-dynamic', 'test','inputPoolkey', 'utils')
    print(engine_path)
    print(rpc_url)
    sys.path.append(engine_path)
    import getOffchainPrice
    token0_symbol = getOffchainPrice.get_token_symbol_from_rpc(rpc_url, token0_address).strip()
    token1_symbol = getOffchainPrice.get_token_symbol_from_rpc(rpc_url, token1_address).strip()
    
    price = getOffchainPrice.fetch_token_price(token0_symbol, token1_symbol)
    result = result.stdout.split("\n")
    print(result)
    
    data = []
    for i in range(len(result) -1):
        tmp = {}
        tmp["name"] = result[i].replace(" ","").split(":")[0]
        tmp["value"] = result[i].replace(" ", "").split(":")[1]
        data.append(tmp)
    print(price)
    print("result")
    print(result)
    ret = {}
    ret["name"] = "Price-compare-using-Pyth"
    ret["data"] = data
    ret["price"] = price
    return ret


def getChkOnlyByPoolManager(result):
    
    realRet = foundryTestParse(result)
    realRet["name"] = "OnlyByPoolManager-Chk"
    for i in range(len(realRet["testList"])):
        if(realRet["testList"][i]["status"] == "FAIL"):
            realRet["testList"][i]["description"] = realRet["testList"][i]["msg"].split("[FAIL: revert: ")[1].split("] ")[0]
    return realRet


def timeTestUsingStep(result):
    ret = {}
    res = result.stdout
    print(res)
    ret["revertAt"] = ""
    ret["name"] = "time-based-step-test"
    try:
        if ("[FAIL: " in res):
            tmp = res.split("time-test-")
            times = tmp[1].split(" Start.")[0]
            print(len(tmp))
            tmp = tmp[len(tmp)-1]
            re = tmp.split('warp end")')[1]
            re = re.split("Suite result:")[0]
            print("time : {}".format(times))
            print(re)
            ret["revertAt"] = times
            ret["trace"] = re
            ret["result"] = "time lock detection at {}".format(times)
        else:
            ret["revertAt"] = None
            ret["result"] = "time lock test clear!"
            ret["trace"] = ""
    except:
        ret["out"] = res

    return ret