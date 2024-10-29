from task.config import app
from celery.result import AsyncResult, GroupResult
def settingData(tmp):
    ret = {}
    reParse = {
        "with_6909" : {},
        "with_20" : {}
    }
    #ret["t"] = tmp
    #print(tmp["result"]["data"].items())
    reParse["with_20"]["swap"] = []
    reParse["with_6909"]["swap"] = []
    ret["name"] = tmp["result"]["name"]
    ret["mode"] = tmp["mode"]
    ret["idx"] = tmp["idx"]
    ret["mode"] = tmp["idx"]
    ret["time"] = tmp["time"]
    ret["poolKey"] = tmp["poolKey"]
    for i, j in tmp["result"]["data"].items():
        if "6909" in i:
            if "addLiquidity" in i:
                reParse["with_6909"]["addLiquidity"] = j
            if "removeLiquidity" in i:
                reParse["with_6909"]["removeLiquidity"] = j
            if "SWAP" in i:
                j["is_burn"] = False
                j["is_exactIn"] = False                    
                if "exactIn" in i:
                    j["is_exactIn"] = True
                if "Burn" in i:
                    j["is_burn"] = True

                reParse["with_6909"]["swap"].append(j)
        else:
            if "addLiquidity" in i:
                reParse["with_20"]["addLiquidity"] = j
            if "removeLiquidity" in i:
                reParse["with_20"]["removeLiquidity"] = j
            if "Donate" in i:
                reParse["with_20"]["donate"] = j
            if "SWAP" in i:
                j["is_burn"] = False
                j["is_exactIn"] = False                    
                if "exactIn" in i:
                    j["is_exactIn"] = True
                if "Burn" in i:
                    j["is_burn"] = True
                print("========")
                print(i)
                print(j)
                reParse["with_20"]["swap"].append(j)
            
                #reParse["with_20"]["swap"].append()
                #   is_6909: boolean;
                #     is_burn: boolean;
                #     is_exactIn: boolean;
                

    ret["data"] = reParse
    #ret["data"] = tmp["result"]
    #print(tmp["result"])
    ret["price"] = tmp["result"]["price"]

    

    return ret
def getTask(task_id):
    result = AsyncResult(task_id, app=app)
    try:
        print("qweqweq")
        print(f"Task Status: {result.status}")
        if result.state == "PENDING":
            print("pending....")
            return {"task_id": task_id, "status": "Pending"}
        elif result.state == "FAILURE":
            return {"task_id": task_id, "status": "Failure"}
        elif result.state == "SUCCESS":
            ret = result.result
            print(ret)
            if(ret["mode"] == 3 ):
                return {"task_id": task_id, "status": "Success", "result": ret}
            if(ret["idx"] == 3):
                ret = settingData(ret)
                print("this")
            #print(f"Task result: {result.result}")
            return {"task_id": task_id, "status": "Success", "result": ret}
        else:
            return {"task_id": task_id, "status": result.state}
    except Exception as f:
        print(f)
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