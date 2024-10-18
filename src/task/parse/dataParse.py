import os
import sys

def hookCompareParse(result):
    result = result.stdout.split("\n")
    ret = {}
    for i in range(len(result)-1):
        tmp = result[i].split(" :  ")
        ret[tmp[0].replace(" ","").replace("-using", "")] = tmp[1].replace(" ","")
    return ret

def foundryTestParse(result):
    result = result.stdout.split("Suite result:")[0].split("\n")
    realRet = {}
    ret = []
    p = 0
    f = 0
    for i in range(3, len(result)-1):
        tmp = result[i].split("] ")
        retTmp = {}
        if("[PASS" in tmp[0]): #[PASS
            retTmp["status"] = "PASS"
            retTmp["statusCode"] = "1"
            retTmp["name"] = tmp[1].split(" ")[0]
            p += 1
            ret.append(retTmp)
        if("[FAIL:" in tmp[0]):
            retTmp["status"] = "FAIL"
            retTmp["statusCode"] = "0"
            print(tmp[1])
            retTmp["name"] = tmp[1].split(" ")[0]
            f += 1
            ret.append(retTmp)
    realRet["testList"] = ret
    realRet["PASS"] = p
    realRet["FAIL"] = f
    return realRet

def minimumTestParse(result):
    realRet = foundryTestParse(result)
    realRet["name"] = "Minimum_Test"
    msgs = ["Fail to add liquidity",
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
            "Fail to check emit log, when donate to pool"
            ]
    for i in range(len(realRet["testList"])):
        if(realRet["testList"][i]["status"] == "FAIL"):
            realRet["testList"][i]["description"] = msgs[i]
    return realRet

def timeBasedMinimumTestParse(result):
    realRet = foundryTestParse(result)
    realRet["name"] = "Time-Based-Minimum_Test"
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
    tmp = {}
    data = []
    for i in range(len(result) -1):
        tmp["name"] = result[i].replace(" ","").split(":")[0]
        tmp["value"] = result[i].replace(" ", "").split(":")[1]
        data.append(tmp)
    print(price)
    print("result")
    print(result)
    ret = {}
    ret["name"] = "hook-NoHook-Compare"
    ret["data"] = data
    ret["price"] = price
    return ret


def getChkOnlyByPoolManager(result):
    realRet = foundryTestParse(result)
    realRet["name"] = "OnlyByPoolManager-Chk"
    return realRet


def timeTestUsingStep(result):
    ret = {}
    res = result.stdout
    print(res)
    ret["revertAt"] = ""
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
    ret["name"] = "time-based-step-test"
    return ret