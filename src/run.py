from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from taskMake import staticTaskMake, dynamicTaskMake, analysisTaskMake
from getTask import getTask
import json


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
    try:
        body = json.loads(body)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON data"}
    isContract = body.get("contract") is not None
    isBytecode = body.get("bytecode") is not None
    isSource = body.get("source") is not None
    print(isContract)
    print(isBytecode)
    print(isSource)
    if(isContract and isBytecode and isSource):
        return {
            "msg" : "nono"
        }
    if( (isContract ^ isBytecode ) and isSource ): # 정적 동적
        #그룹을 만들기
        print("1")
        task_info = analysisTaskMake()
    elif(isContract or isBytecode): #동적만
        #동적 테스크 만들기
        task_info = dynamicTaskMake()
        print("2")
    elif(isSource): #정적만
        #정적 테스크 만들기
        task_info = staticTaskMake()
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
    return 'a'