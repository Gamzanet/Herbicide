from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from getTask import getTask
#from analysisSetting import setStaticAnalysis#, setAddressDynamicAnalysis, setOpDynamicAnalysis
import analysisSetting
import json
import hashlib
import time

from resultFind import findTest, _findTest


app = FastAPI()
origins = origins = ["*"]                                                                                                                                                                                                  
app.add_middleware(                                                                               
    CORSMiddleware,                                                                             
    allow_origins=origins,                                                                        
    allow_credentials=True,                                                                      
    allow_methods=["*"],                                                                        
    allow_headers=["*"],                                                                     
)    


@app.get("/")
def read_root(request: Request):
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/result/{task_id}")
def send_result(task_id: str):
    return getTask(task_id)

@app.post("/api/tasks")
async def recv_result(request: Request):
    
    from taskMake import staticTaskMake, dynamicTaskMake, analysisTaskMake, codeStaticTaskMake
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
        testCache = findTest(data["poolKey"], data["mode"])
        analysisSetting.setDynamicAnalysis(timeHash, data["poolKey"], data["deployer"] )
        task_info = dynamicTaskMake( timeHash, 
                                    __import__('os').environ.get('uni'), 
                                    data["poolKey"] )
        print("2")

    elif( data["mode"] == 3 ): #정적만
        #정적 테스크 만들기
        # print(body.get("source"))
        # print(dir(analysisSetting))
        testCache = findTest(data["poolKey"], data["mode"])
        task_info = staticTaskMake(timeHash, data["poolKey"])
        print("3")
    elif( data["mode"] == 4): # 정적 코드만
        codeHash = hashlib.sha256(str(data["source"]).encode()).hexdigest()
        file_path = analysisSetting.setStaticAnalysis(timeHash,codeHash ,data["source"]) #
        task_info = codeStaticTaskMake(timeHash,codeHash, file_path)
        return {
            "msg": "Task created",
            "info" : task_info
        }

    else:
        return{
            "msg" : "nono"
        }
    return {
        "msg": "Task created",
        "info" : task_info,
        "testCache" : testCache
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
    if(not ((mode is not None) and mode >=1 and mode <= 4)):
        return {"status":-1, "error": "Invalid Mode"}
    #Static
    isSource      =  body.get("data").get("source") is not None
    data = {}
    data["mode"]          = mode
    data["status"]          = 1
    if ( mode == 4 and isSource):
        data["source"] = body.get("data").get("source")
        return data
    #Dynamic
    PoolKey = body.get("data").get("Poolkey")
    deployer = body.get("data").get("deployer")
    if (deployer is None):
        deployer = "0x4e59b44847b379578588920cA78FbF26c0B4956C"
    print("PoolKey : {}\n mode : {}".format(PoolKey, mode))

    isHooks       =  PoolKey.get("hooks") is not None
    isCurrency0   =  PoolKey.get("currency0") is not None
    isCurrency1   =  PoolKey.get("currency1") is not None
    isFee         =  PoolKey.get("fee") is not None
    isTickSpacing =  PoolKey.get("tickSpacing") is not None

    if( not(isHooks and isCurrency0 and isCurrency1 and isFee and isTickSpacing) ):
        return {"status":-1, "error": "Invalid Mode"}


    
    

    _poolkey = {}
    _poolkey["hooks"]           = PoolKey.get("hooks")
    _poolkey["currency0"]       = PoolKey.get("currency0")
    _poolkey["currency1"]       = PoolKey.get("currency1")
    _poolkey["fee"]             = PoolKey.get("fee")
    _poolkey["tickSpacing"]     = PoolKey.get("tickSpacing")
    data["poolKey"] = _poolkey
    data["deployer"] = deployer

    return data


from fastapi.responses import StreamingResponse
import time
import asyncio
async def event_stream(t,h, m, finder):
    cnt = 0
    current = []
    while True:
        tests = _findTest(t, h, m, finder)
        print(t, h , m)
        new = [item for item in tests if item not in current]
        current = tests
        print("c")
        print(current)
        print(new)
        print(finder)
        for i in range(len(new)):
            print("send")
            t = "data: complate idx : {}, task-id : {}\n\n".format(new[i]["idx"], new[i]["task_id"])
            yield t
        await asyncio.sleep(1)
        if(len(current) >= len(finder)):
            return
        cnt += 1

@app.get("/api/noti/{timeHash}/{hooks}/{mode}/{cpnt}")
async def get_events(timeHash: str, hooks: str, mode:int, cpnt:int):
    idx = []
    if (mode == 2): # dynamic
        if(cpnt == 0): # price oracle
            idx = [3]
        if(cpnt == 1): # hook nohook compare
            idx = [2]
        if(cpnt == 2): # other tests
            # minimum, timebasedminimum, poolmanager, time-step, 
            # doubleInit, upgradable
            # idx = [0, 1, 4, 5, 6, 7] 
            idx = [0, 1, 4, 6, 7] 
    elif(mode == 3):
        idx = [0]
    elif(mode == 4):
        idx = [0]

    return StreamingResponse(event_stream(timeHash, hooks, mode, idx), media_type="text/event-stream")

@app.get("/a")
def read_root(request: Request):
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("a.html", {"request": request})
