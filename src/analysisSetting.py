#/bin/python
import subprocess
import os
def setStaticAnalysis(task_id, source):
    #file_path = os.path.expanduser(f"~/tmp/{12}")
    file_path = os.path.expanduser(f"~/tmp/{task_id}.sol")
    with open(file_path, "w") as f:
        f.write(source)
    
def setOpDynamicAnalysis(task_id, opcode):
    a = 1
    #result = subprocess.run("cast send --create {} --private-key $anvil_pk".format(opcode), shell=True, capture_output=True, text=True)
    #확인하는 로직 해야함
    #result = subprocess.run("".format(opcode), shell=True, capture_output=True, text=True)

def setDynamicAnalysis(task_id, address):
    a = 1
    #result = subprocess.run("cast send --create {} --private-key $anvil_pk".format(opcode), shell=True, capture_output=True, text=True)
    #확인하는 로직 해야함
    #result = subprocess.run("".format(opcode), shell=True, capture_output=True, text=True)
