from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from taskMake import staticTaskMake, dynamicTaskMake, analysisTaskMake
from getTask import getTask
#from analysisSetting import setStaticAnalysis#, setAddressDynamicAnalysis, setOpDynamicAnalysis
import analysisSetting
import json
import hashlib
import time


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/result/{task_id}")
def send_result(task_id: str):
    return getTask(task_id)

@app.post("/api/tasks")
async def recv_result(request: Request):
    
    body = await request.body()
    print(body)
    data = validation(body)
    
    print(data)
    if( data["status"] == -1 ):
        return {
            "msg" : "nono"
        }
    timeHash = hashlib.sha256(str(int(time.time())).encode()).hexdigest()
    if( data["mode"] == 1 ): # 정적 동적
        #그룹을 만들기 # 병렬말고 직렬로 하도록?
        print("1")
        task_info = analysisTaskMake()

    elif( data["mode"] == 2 ): #동적만
        #동적 테스크 만들기
        analysisSetting.setDynamicAnalysis(timeHash, 
                                           data["currency0"], 
                                           data["currency1"], 
                                           data["fee"], 
                                           data["tickSpacing"], 
                                           data["hooks"] )
        
        task_info = dynamicTaskMake( timeHash, __import__('os').environ.get('uni'), data["currency0"], data["currency1"] )
        print("2")

    elif( data["mode"] == 3 ): #정적만
        #정적 테스크 만들기
        # print(body.get("source"))
        # print(dir(analysisSetting))
        # analysisSetting.setStaticAnalysis(timeHash, body.get("source")) # 현재상황 소스 안받는것을 가정으로
        task_info = staticTaskMake(timeHash, data["hooks"])
        print("3")

    else:
        return{
            "msg" : "nono"
        }
    return {
        "msg": "Task created",
        "info" : task_info
    }
@app.get("/api/result/g/{group_id}")
def get_task_group_status(group_id: str):
    # groupID는 당장은 보류하는 것으로.. 
    return 'a'

def validation(body):
    try:
        body = json.loads(body)
    except json.JSONDecodeError:
        return {"status":-1,"error": "Invalid JSON data"}
    
    #print( body.get("data").get("cocoa") )

    mode = body.get("data").get("mode")
    if(not ((mode is not None) and mode >=1 and mode <= 3)):
        return {"status":-1, "error": "Invalid Mode"}
    #Static
    isSource      =  body.get("source") is not None
    #Dynamic
    PoolKey = body.get("data").get("Poolkey")
    print("PoolKey : {}\n mode : {}".format(PoolKey, mode))

    isHooks       =  PoolKey.get("hooks") is not None
    isCurrency0   =  PoolKey.get("currency0") is not None
    isCurrency1   =  PoolKey.get("currency1") is not None
    isFee         =  PoolKey.get("fee") is not None
    isTickSpacing =  PoolKey.get("tickSpacing") is not None

    if( not(isHooks and isCurrency0 and isCurrency1 and isFee and isTickSpacing) ):
        return {"status":-1, "error": "Invalid Mode"}

    
    
    data = {}
    data["mode"]          = mode
    data["status"]          = 1
    data["hooks"]           = PoolKey.get("hooks")
    data["currency0"]       = PoolKey.get("currency0")
    data["currency1"]       = PoolKey.get("currency1")
    data["fee"]             = PoolKey.get("fee")
    data["tickSpacing"]     = PoolKey.get("tickSpacing")
    return data