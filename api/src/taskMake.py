
from task.tasks import analysis

def taskMake():
    result = analysis.delay(4, 6)
    res = {
        "status": 0, 
        "id": result.id,  
        "detail": result.status  
    }
    print(f"Task Created: {res}")

    return res