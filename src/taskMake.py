
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

def dynamicTaskMake(timeHash, rpc, c0, c1):
    result = dynamic.delay(timeHash, rpc, c0, c1)
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
