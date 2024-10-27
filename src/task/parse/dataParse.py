import os
import sys
import re

def hookCompareParse(result):
    result = result.stdout.split("\n")
    ret = {}
    ret["name"] = "hook-NoHook-Compare"
    ret["msg"] = result
    for i in range(len(result)-1):
        tmp = result[i].split(" :  ")
        ret[tmp[0].replace(" ","").replace("-using", "")] = (tmp[1].replace(" ",""))
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
    import getSwapPrice

    token0_symbol = getOffchainPrice.get_token_symbol_from_rpc(rpc_url, token0_address).strip()
    token1_symbol = getOffchainPrice.get_token_symbol_from_rpc(rpc_url, token1_address).strip()
    
    price = getOffchainPrice.fetch_token_price(token0_symbol, token1_symbol)
    namelist = [
        "addLiquidity6909-","addLiquidity-",
        "Donate-",
        "removeLiquidity6909-","removeLiquidity-",
        "SWAP-exactIn Burn 6909", "SWAP-exactIn Mint 6909", 
        "SWAP-exactIn-", "SWAP-exactOut Burn 6909", 
        "SWAP-exactOut Mint 6909", "SWAP-exactOut-"
    ]

    result = result.stdout
    tmp = {}
    for i in range(len(namelist)):
        find = re.findall(r'{}.*'.format(namelist[i]), result, re.MULTILINE)
        r = []
        t = {}
        for j in range(len(find)):
            # print(j)
            # print(passed[j])
            find[j] = find[j].replace("{}".format(namelist[i]),"")
            key = find[j].split(":")[0].replace(" ","")
            val = find[j].split(":")[1].replace(" ","")
            #print(passed[j].split(":")[1].replace(" ","")[0])
            if key[0] == '-':
                #print("qweqeq")
                key = key[1:]
            t[key] = val
        namelist[i] = namelist[i].replace(" ","-")
        if(namelist[i][-1] == "-"):
            namelist[i] = namelist[i][:len(namelist[i])-1]
        tmp[namelist[i]] = t
        t = {}
    ret = {}
    for i in range(len(namelist)):
      # calc_expected(price_current, liquidity,specified,fee):
        if("SWAP-exact" in namelist[i]):
            calc_value = getSwapPrice.calc_expected(
                tmp[namelist[i]]["for-expected-current-price"] , 
                tmp[namelist[i]]["for-expected-current-liquidity"], 
                tmp[namelist[i]]["for-expected-amount0-specified"], 
                tmp[namelist[i]]["for-expected-current-fee"]
            )
            tmp[namelist[i]]["calc"] = {}
            tmp[namelist[i]]["calc"]["price_expected"] = calc_value[0]
            tmp[namelist[i]]["calc"]["sqrtP_expected"] = calc_value[1]
            tmp[namelist[i]]["calc"]["amount_in"] = calc_value[2]
            tmp[namelist[i]]["calc"]["amount_out"] = calc_value[3]
    #ret["msg"] = result
    ret["name"] = "Price-compare-using-Pyth"
    ret["data"] = tmp
    ret["price"] = price
    return ret


def getChkOnlyByPoolManager(result):
    
    realRet = foundryTestParse(result)
    realRet["name"] = "OnlyByPoolManager-Chk"
    for i in range(len(realRet["testList"])):
        try:
            if(realRet["testList"][i]["status"] == "FAIL"):
                realRet["testList"][i]["description"] = realRet["testList"][i]["msg"].split("[FAIL: revert: ")[1].split("] ")[0]
        except:
            realRet["testList"][i]["description"] = realRet["testList"][i]["msg"]
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
            times = res.split("Traces:")[0].split("Start.")[-2].split("time-test-")[-1]
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
def doubleInitParse(result):
    response = {}
    log_data = result.stdout.replace("  ","")
    response["name"] = "double-Initialize-Test"
    # 정규식을 이용해 slot-write-N, prev_value, old_value, new_value 매칭
    pattern = re.compile(r'slot-write-(\d+)\n(0x[0-9a-fA-F]{64})\n(0x[0-9a-fA-F]{64})\n(0x[0-9a-fA-F]{64})\n(0x[0-9a-fA-F]{40})\n(0x[0-9a-fA-F]{40})\n')
    # defaultdict로 slot 데이터 저장
    slot_data = [[],[]]

    # 정규식으로 매칭된 데이터 추출
    for match in pattern.finditer(log_data):
        slot_number = int(match.group(1))  # slot-write-N의 N 값
        entry = {
            "slot" : match.group(2),           # slot 값
            "prev_value" : match.group(3),     # prevValue
            "new_value" : match.group(4),       # newValue
            "access_to" : match.group(5),       # account
            "contract" : match.group(6)       # contract
        }
        slot_data[slot_number].append(entry)  # slot_write-N에 데이터 추가
    ret = []
    if len(slot_data[0])!= 0 and len(slot_data[1])!= 0:
        set1 = {(entry["slot"], entry["contract"]) for entry in slot_data[0]}
        set2 = {(entry["slot"], entry["contract"]) for entry in slot_data[1]}
        common_slots = set1 & set2  # 중복된 slot 값 찾기
        if common_slots:
            response["status"] = 1
            for slot, contract in common_slots:
                tmp = {"k1" : {}, "k2" : {}}
                f = {"k1":0, "k2": 0}
                for entry in slot_data[0]:
                    if entry["slot"] == slot and entry["contract"] == contract:
                        tmp["k1"]["prev_value"] = entry["prev_value"]
                        tmp["k1"]["new_value"] = entry["new_value"]
                        # tmp["k1"]["access_to"] = entry["access_to"]
                        # tmp["k1"]["contract"] = entry["contract"]
                        f["k1"] = 1
                for entry in slot_data[1]:
                    if entry["slot"] == slot and entry["contract"] == contract:
                        tmp["k2"]["prev_value"] = entry["prev_value"]
                        tmp["k2"]["new_value"] = entry["new_value"]
                        # tmp["k2"]["access_to"] = entry["access_to"]
                        #tmp["k2"]["contract"] = entry["contract"]
                        f["k2"] = 1
                if(f["k1"] == 1 and f["k2"] == 1):
                    tmp["slot"] = slot
                    tmp["contract"] = contract
                    ret.append(tmp)
        else:
            response["status"] = 0
    else:
        response["status"] = -1
        
    response["data"] = ret
    return response

def upgradableParse(result):
    realRet = foundryTestParse(result)
    realRet["name"] = "Proxy-Test"
    return realRet