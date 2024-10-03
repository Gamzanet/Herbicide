from task.config import app
from celery.result import AsyncResult


task_id = "045a595b-fd0c-4f52-92c8-26c8d4d945f6"
result = AsyncResult(task_id, app=app)
print(f"Task Status: {result.status}")
if result.successful():
    print(f"Result: {result.get()}")
else:
    print("Task is not successful or failed.")
