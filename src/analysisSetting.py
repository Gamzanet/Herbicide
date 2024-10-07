#/bin/python
import subprocess
import os
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
    data = '''{
    "data": {
    "currency0": {},
    "currency1": {},
    "fee": {},
    "tickSpacing": {},
    "hooks": {}
    }
}'''.format(currency0, currency1, fee, tickSpacing, hooks)
    file_path = os.path.expanduser(f"~/tmp/dynamic_{timeHash}.json")
    with open(file_path, "w") as f:
        f.write(data)
    
    #result = subprocess.run("cast send --create {} --private-key $anvil_pk".format(opcode), shell=True, capture_output=True, text=True)
    #확인하는 로직 해야함
    #result = subprocess.run("".format(opcode), shell=True, capture_output=True, text=True)
