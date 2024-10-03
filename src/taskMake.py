
from task.tasks import analysis, dynamic, static
from celery import group
def staticTaskMake():
    result = static.delay(6)
    res = {
        "status": 0, 
        "id": result.id,  
        "detail": result.status  
    }
    print(f"Task Created: {res}")
    return res

def dynamicTaskMake():
    result = dynamic.delay(4)
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
