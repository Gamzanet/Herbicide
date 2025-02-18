from typing import Dict, Any
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
import json
import hashlib
import time
import asyncio

# 내부 모듈 임포트
from getTask import getTask
from task.threadWork import testRun
import analysisSetting
from resultFind import findTest, _findTest
from taskMake import staticTaskMake, dynamicTaskMake, analysisTaskMake, codeStaticTaskMake

# FastAPI 인스턴스 생성
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# ✅ 루트 페이지
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ 특정 Task 결과 조회
@app.get("/api/result/{task_id}")
def send_result(task_id: str):
    return getTask(task_id)

# ✅ Task 생성 (POST 요청)
@app.post("/api/tasks")
async def create_task(request: Request):
    body = await request.body()
    data = validate_request(body)

    if data["status"] == -1:
        return {"msg": "Invalid request"}

    time_hash = hashlib.sha256(str(int(time.time())).encode()).hexdigest()
    
    if data["mode"] == 1:  # 정적 + 동적 분석
        task_info = analysisTaskMake()

    elif data["mode"] == 2:  # 동적 분석만
        rpc = __import__('os').environ.get('local')   # rpc-url
        testCache = findTest(data["poolKey"], data["mode"])
        
        valid = testRun(f"cast call --rpc-url {rpc} {data['poolKey']['hooks']} \"poolManager()\"")
        if len(valid.stdout.strip()) != 66 or len(valid.stderr) != 0:
            return {"msg": "Not a valid hook"}

        analysisSetting.setDynamicAnalysis(time_hash, data["poolKey"], data["deployer"])
        task_info = dynamicTaskMake(time_hash, rpc, data["poolKey"])

    elif data["mode"] == 3:  # 정적 분석만
        testCache = findTest(data["poolKey"], data["mode"])
        task_info = staticTaskMake(time_hash, data["poolKey"])

    elif data["mode"] == 4:  # 정적 코드 분석
        code_hash = hashlib.sha256(str(data["source"]).encode()).hexdigest()
        file_path = analysisSetting.setStaticAnalysis(time_hash, code_hash, data["source"])
        task_info = codeStaticTaskMake(time_hash, code_hash, file_path)
        return {"msg": "Task created", "info": task_info}

    else:
        return {"msg": "Invalid mode"}

    return {"msg": "Task created", "info": task_info, "testCache": testCache}

# ✅ Task Group 조회 (보류)
@app.get("/api/result/g/{group_id}")
def get_task_group_status(group_id: str):
    return "Not implemented yet"

# ✅ 요청 데이터 유효성 검사
def validate_request(body: bytes) -> Dict[str, Any]:
    try:
        body = json.loads(body)
    except json.JSONDecodeError:
        return {"status": -1, "error": "Invalid JSON"}

    mode = body.get("data", {}).get("mode")
    if mode not in {1, 2, 3, 4}:
        return {"status": -1, "error": "Invalid mode"}

    data = {"mode": mode, "status": 1}

    if mode == 4 and body["data"].get("source"):
        data["source"] = body["data"]["source"]
        return data

    pool_key = body.get("data", {}).get("Poolkey", {})
    deployer = body.get("data", {}).get("deployer", "0x4e59b44847b379578588920cA78FbF26c0B4956C")

    required_keys = {"hooks", "currency0", "currency1", "fee", "tickSpacing"}
    if not required_keys.issubset(pool_key.keys()):
        return {"status": -1, "error": "Invalid PoolKey structure"}

    data["poolKey"] = {key: pool_key[key] for key in required_keys}
    data["deployer"] = deployer
    return data

# ✅ 비동기 이벤트 스트리밍 (Task 상태 업데이트)
async def event_stream(time_hash: str, hooks: str, mode: int, expected_tasks: list):
    current = []
    while True:
        tests = _findTest(time_hash, hooks, mode, expected_tasks)
        new_tasks = [item for item in tests if item not in current]
        current = tests

        for task in new_tasks:
            yield f"data: complete idx: {task['idx']}, task-id: {task['task_id']}\n\n"

        await asyncio.sleep(1)
        if len(current) >= len(expected_tasks):
            return

# ✅ 특정 Task 상태를 SSE로 제공
@app.get("/api/noti/{timeHash}/{hooks}/{mode}/{cpnt}")
async def get_events(timeHash: str, hooks: str, mode: int, cpnt: int):
    index_map = {
        2: {0: [3], 1: [2], 2: [0, 1, 4, 6, 7]},  # Dynamic Analysis
        3: [0],  # Static Analysis
        4: [0],  # Code Analysis
    }
    tasks = index_map.get(mode, {}).get(cpnt, [])
    return StreamingResponse(event_stream(timeHash, hooks, mode, tasks), media_type="text/event-stream")

# ✅ 테스트용 페이지
@app.get("/a")
def read_root(request: Request):
    return templates.TemplateResponse("a.html", {"request": request})