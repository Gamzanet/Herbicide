import redis
import json
from datetime import datetime, timedelta, timezone
def findTest(poolkey, mode):
    r = redis.Redis(host='localhost', port=6379, db=0)
    all_keys = r.keys('*')
    print(all_keys)
    
    retArr = []
    for key in all_keys:
        # print(key.decode('utf-8'))
        res = r.get(key)
        ret = {}
        try:
            tmp = json.loads(res)
            if(tmp["result"]["poolKey"] == poolkey and tmp["result"]["mode"] == mode):
                print("find!")
                # print(tmp)
                ret["task_id"] = tmp["task_id"]
                utc_datetime = datetime.fromisoformat(tmp["date_done"])
                ret["date_done"] = str(utc_datetime.astimezone(timezone(timedelta(hours=9))))[:19]
                # ret["poolkey"] = tmp["result"]["poolkey"]
                # ret["mode"] = tmp["result"]["mode"]
                # ret["status"] = 1
                retArr.append(ret)
        except:
            print("err")
    return retArr
def _findTest(timeHash, hooks,  mode, idx):
    r = redis.Redis(host='localhost', port=6379, db=0)
    all_keys = r.keys('*')
    print(all_keys)
    retArr = []
    for key in all_keys:
        # print(key.decode('utf-8'))
        res = r.get(key)
        ret = {}
        try:
            tmp = json.loads(res)
            for i in range(len(idx)):
                if(tmp["result"]["poolkey"]["hooks"] == hooks and tmp["result"]["mode"] == mode and tmp["result"]["timeHash"] == timeHash and tmp["result"]["idx"] == idx[i]):
                    ret["task_id"] = tmp["task_id"]
                    ret["idx"] = tmp["result"]["idx"]
                    utc_datetime = datetime.fromisoformat(tmp["date_done"])
                    ret["date_done"] = str(utc_datetime.astimezone(timezone(timedelta(hours=9))))[:19]
                    retArr.append(ret)
        except Exception as e:
            print("err")
            print(e)
    return retArr

if __name__ =="__main__":
    p = { 
        "currency0" : "0x6aD83000194DFCf9a0869091B2Ea7D121033163E", 
        "currency1" : "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
        "fee" : 0, 
        "tickSpacing" : 60, 
        "hooks": "0xF20Ac4669fc2bbAC775B46875E22Ba851bF64AC0"
    }
    t = "7a85b85a16191aa652f80c39ba879d105be377279853214ec9f1efce6a4e364a"
    a = _findTest(t, p["hooks"], 2, [3])
    print(len(a))
    for i in range(len(a)):
        print(a[i])
