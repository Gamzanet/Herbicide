
from task.tasks import analysis, dynamic, static, dynamic_minimum, dynamic_timeBasedMinimumTest, dynamic_hookCompare, dynamic_priceCheck,dynamic_OnlyByPoolManager, dynamic_timeTestUsingStep, dynamic_doubleInit, dynamic_upgradable
from celery import group
def staticTaskMake(timeHash, hook):
    result = static.delay(timeHash, hook)
    res = {
        "hooks" : hook,
        "timeHash" : timeHash,
        "tasks" : [{"id": result.id, "stat" : result.status}]
    }
    print(f"Task Created: {res}")
    return res

def dynamicTaskMake(timeHash, rpc,poolkey):
    ids = []

    key = dynamic_minimum.delay(timeHash, rpc, poolkey, 0) # 0
    ids.append({"id" : key.id, "stat" : key.status}) 
    key = dynamic_timeBasedMinimumTest.delay(timeHash, rpc, poolkey, 1) #1
    ids.append({"id" : key.id, "stat" : key.status})
    key = dynamic_hookCompare.delay(timeHash, rpc, poolkey, 2) #2
    ids.append({"id" : key.id, "stat" : key.status})
    key = dynamic_priceCheck.delay(timeHash, rpc, poolkey, 3) #3
    ids.append({"id" : key.id, "stat" : key.status})
    key = dynamic_OnlyByPoolManager.delay(timeHash, rpc, poolkey, 4) #4
    ids.append({"id" : key.id, "stat" : key.status})
    key = dynamic_timeTestUsingStep.delay(timeHash, rpc, poolkey, 5) #5
    ids.append({"id" : key.id, "stat" : key.status})
    key = dynamic_doubleInit.delay(timeHash, rpc, poolkey, 6) #6
    ids.append({"id" : key.id, "stat" : key.status}) 
    key = dynamic_upgradable.delay(timeHash, rpc, poolkey, 7) #7
    ids.append({"id" : key.id, "stat" : key.status})
    res = {
        "hooks" : poolkey["hooks"],
        "timeHash" : timeHash,
        "tasks" : ids
    }
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

# def dynamicTaskMake(timeHash, rpc,poolkey):
#     result = dynamic.delay(timeHash, rpc, poolkey)
#     res = {
#         "status": 0, 
#         "id": result.id,  
#         "hooks" : poolkey["hooks"],
#         "detail": result.status  
#     }
#     print(f"Task Created: {res}")
#     return res