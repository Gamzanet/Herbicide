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

def setDynamicAnalysis(timeHash, currency0, currency1, fee, tickSpacing, hooks):
    data = {
        "data": {
            "currency0": currency0,
            "currency1": currency1,
            "fee": fee,
            "tickSpacing": tickSpacing,
            "hooks": hooks
        }
    }
    file_path = os.path.expanduser(f"~/tmp/dynamic_{timeHash}.json")
    engine_path = os.path.join('engine', 'gamza-dynamic','test',"_json_TakeProfitsHook.json" )#f"dynamic_{timeHash}.json")
    print(os.system("pwd"))
    print(engine_path)
    with open(engine_path, "w") as f:
        json.dump(data, f)
    
    #result = subprocess.run("cast send --create {} --private-key $anvil_pk".format(opcode), shell=True, capture_output=True, text=True)
    #확인하는 로직 해야함
    #result = subprocess.run("".format(opcode), shell=True, capture_output=True, text=True)
