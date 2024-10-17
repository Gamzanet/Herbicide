
from task.tasks import analysis, dynamic, static
from celery import group
def staticTaskMake(hash):
    result = static.delay(hash)
    res = {
        "status": 0, 
        "id": result.id,  
        "detail": result.status  
    }
    print(f"Task Created: {res}")
    return res

def dynamicTaskMake(rpc):
    base_rpc = "https://base-sepolia.blockpi.network/v1/rpc/public"
    base_rpc = "https://base-sepolia.infura.io/v3/33c8211714a74336b1af760a211c7037"
    result = dynamic.delay(base_rpc)
    res = {
        "status": 0, 
        "id": result.id,  
        "detail": result.status  
    }
    print(f"Task Created: {res}")
    return res

def analysisTaskMake():
    result = analysis.delay(4,2)
    res = {
        "status": 0, 
        "id": result.id,  
        "detail": result.status  
    }
    print(f"Task Created: {res}")
    return res
