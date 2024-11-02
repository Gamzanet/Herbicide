#/bin/python
import subprocess
import os
import hashlib

import json
def setStaticAnalysis(timeHash, codeHash, source):
    src = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(src, "data","static_{}_{}.sol".format(timeHash,codeHash))
    with open(file_path, "w") as f:
        f.write(source)
    return file_path
    
def setOpDynamicAnalysis(task_id, opcode):
    a = 1
    #result = subprocess.run("cast send --create {} --private-key $anvil_pk".format(opcode), shell=True, capture_output=True, text=True)
    #확인하는 로직 해야함
    #result = subprocess.run("".format(opcode), shell=True, capture_output=True, text=True)

def setDynamicAnalysis(timeHash, poolkey,deployer ):
    data = {
        "data": {
            "currency0": poolkey["currency0"], 
            "currency1": poolkey["currency1"], 
            "fee": poolkey["fee"], 
            "tickSpacing": poolkey["tickSpacing"], 
            "hooks": poolkey["hooks"], 
        },
        "deployer": deployer
    }
    src = os.path.dirname(os.path.abspath(__file__))
    engine_path = os.path.join(src, "data","dynamic_{}_{}.json".format(timeHash,poolkey["hooks"]))
    print("engine : {}".format(engine_path))
    with open(engine_path, "w") as f:
        json.dump(data, f)
