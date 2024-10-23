
from task.tasks import analysis, dynamic, static
from celery import group
def staticTaskMake(timeHash, hook):
    result = static.delay(timeHash, hook)
    res = {
        "status": 0, 
        "id": result.id,  
        "detail": result.status  
    }
    print(f"Task Created: {res}")
    return res

def dynamicTaskMake(timeHash, rpc,poolkey):
    result = dynamic.delay(timeHash, rpc, poolkey)
    res = {
        "status": 0, 
        "id": result.id,  
        "hooks" : poolkey["hooks"],
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
