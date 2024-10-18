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
    try:
        body = json.loads(body)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON data"}
    
    #print( body.get("data").get("cocoa") )
    print( body.get("source") )
    print( body.get("currency0") )
    print( body.get("currency1") )
    print( body.get("fee") )
    print( body.get("tickSpacing") )
    print( body.get("hooks") )

    
    #Static
    isSource      =  body.get("source") is not None

    #Dynamic
    data = body.get("data")

    isHooks       =  body.get("hooks") is not None
    isCurrency0   =  body.get("currency0") is not None
    isCurrency1   =  body.get("currency1") is not None
    isFee         =  body.get("fee") is not None
    isTickSpacing =  body.get("tickSpacing") is not None
    

    if( (isHooks or isCurrency0 or isCurrency1 or isFee or isTickSpacing) and isSource):
        return {
            "msg" : "nono"
        }
    timeHash = hashlib.sha256(str(int(time.time())).encode()).hexdigest()
    if( (isHooks and isCurrency0 and isCurrency1 and isFee and isTickSpacing ) and isSource ): # 정적 동적
        #그룹을 만들기 # 병렬말고 직렬로 하도록?
        print("1")
        task_info = analysisTaskMake()

    elif( (isHooks and isCurrency0 and isCurrency1 and isFee and isTickSpacing ) and not isSource): #동적만
        #동적 테스크 만들기
        analysisSetting.setDynamicAnalysis(timeHash, 
                                           body.get("currency0"), 
                                           body.get("currency1"), 
                                           body.get("fee"), 
                                           body.get("tickSpacing"), 
                                           body.get("hooks")  )
        task_info = dynamicTaskMake(timeHash, __import__('os').environ.get('uni'), body.get("currency0"), body.get("currency1"))
        print("2")

    elif(isSource and not (isHooks or isCurrency0 or isCurrency1 or isFee or isTickSpacing) ): #정적만
        #정적 테스크 만들기
        print(body.get("source"))
        print(dir(analysisSetting))
        analysisSetting.setStaticAnalysis(timeHash, body.get("source"))
        task_info = staticTaskMake(timeHash)
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