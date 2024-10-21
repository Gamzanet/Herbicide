from task.config import app
from celery.result import AsyncResult, GroupResult

def getTask(task_id):
    result = AsyncResult(task_id, app=app)
    try:
        print(f"Task Status: {result.status}")
        if result.state == "PENDING":
            print("pending....")
            return {"task_id": task_id, "status": "Pending"}
        elif result.state == "FAILURE":
            return {"task_id": task_id, "status": "Failure"}
        elif result.state == "SUCCESS":
            print(f"Task result: {result.result}")
            return {"task_id": task_id, "status": "Success", "result": result.result}
        else:
            return {"task_id": task_id, "status": result.state}
    except:
        return{"task_id": task_id, "status":"result not found"}
    
def getGroupTask(group_id):
    group_result = GroupResult(group_id, app=app)
    
    if group_result is None:
        print(f"그룹 {group_id}를 찾을 수 없습니다.")
        return

    print("Group Result:", group_result)
    print("Group ID:", group_result.id)
    print("Group Ready:", group_result.children)
    print("Group Successful:", group_result.successful())

    # 개별 작업 결과 확인
    for task_id in group_result.children:
        task_result = AsyncResult(task_id)
        print(f"Task ID: {task_id}")
        print(f"Task State: {task_result.state}")
        print(f"Task Result: {task_result.result}")
        print("---")

    # 모든 작업 결과 한 번에 가져오기
    all_results = group_result.get(timeout=10)  # 10초 타임아웃 설정
    print("All Results:", all_results)

if __name__ == "__main__":
    getGroupTask("d7e3b019-688d-4f54-a0a7-4114be1dcd47")