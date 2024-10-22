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
            if(tmp["result"]["poolkey"] == poolkey and tmp["result"]["mode"] == mode):
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

if __name__ =="__main__":
    p = { 
        "currency0" : "0x6aD83000194DFCf9a0869091B2Ea7D121033163E", 
        "currency1" : "0xe61398b1Cb0FBED8268808A983Ad71ECFE2e1Ee9",
        "fee" : 0, 
        "tickSpacing" : 60, 
        "hooks": "0x15F3F147eB0278b46363529083751363Be248c00"
    }
    a = findTest(p,2)
    print(a)