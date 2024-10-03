from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from taskMake import taskMake
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/result")
def send_result(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) 

@app.post("/api/tasks")
def recv_result():
    task_info = taskMake()
    return {
        "message": "Task created",
        "task_id": task_info["id"]
    }