#/bin/python
import subprocess
import os
import json
def setStaticAnalysis(timeHash, source):
    #file_path = os.path.expanduser(f"~/tmp/{12}")
    file_path = os.path.expanduser(f"~/tmp/static_{timeHash}.sol")
    with open(file_path, "w") as f:
        f.write(source)
    
def setOpDynamicAnalysis(task_id, opcode):
    a = 1
    #result = subprocess.run("cast send --create {} --private-key $anvil_pk".format(opcode), shell=True, capture_output=True, text=True)
    #확인하는 로직 해야함
    #result = subprocess.run("".format(opcode), shell=True, capture_output=True, text=True)

def setDynamicAnalysis(timeHash, poolkey):
    data = {
        "data": {
            "currency0": poolkey["currency0"], 
            "currency1": poolkey["currency1"], 
            "fee": poolkey["fee"], 
            "tickSpacing": poolkey["tickSpacing"], 
            "hooks": poolkey["hooks"], 
        }
    }
    engine_path = os.path.join("data","dynamic_{}_{}.json".format(timeHash,poolkey["hooks"]))#f"dynamic_{timeHash}.json")
    print(engine_path)
    with open(engine_path, "w") as f:
        json.dump(data, f)
    
    #result = subprocess.run("cast send --create {} --private-key $anvil_pk".format(opcode), shell=True, capture_output=True, text=True)
    #확인하는 로직 해야함
    #result = subprocess.run("".format(opcode), shell=True, capture_output=True, text=True)
