import os
import sys

def hookCompareParse(result):
    result = result.stdout.split("\n")
    ret = {}
    for i in range(len(result)-1):
        tmp = result[i].split(" :  ")
        ret[tmp[0].replace(" ","").replace("-using", "")] = tmp[1].replace(" ","")
    return ret

def minimumTestParse(result):
    result = result.stdout.split("\n")
    ret = []
    for i in range(2, len(result)-1):
        ret.append(result[i])
    return ret
def timeBasedMinimumTestParse(result):
    result = result.stdout.split("\n")
    ret = []
    for i in range(2, len(result) -1):
        ret.append(result[i])
    return ret
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
    for i in range(len(result) -1):
        tmp[result[i].replace(" ","").split(":")[0]] = result[i].replace(" ", "").split(":")[1]
    print(price)
    print("result")
    print(result)
    ret = {}
    ret["stdout"] = tmp
    ret["price"] = price
    return ret

