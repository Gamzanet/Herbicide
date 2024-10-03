from task.tasks import analysis

# 작업 호출 (비동기)
print("start")
result = analysis.delay(4, 6)
print()
print(f"Task ID: {result.id}")

while not result.ready():
    a = 1
    print(f"Task Status: {result.status}")
    print(f"Task ID: {result.id}")

# 결과 확인
if result.successful():
    print(f"Task Status: {result.status}")
    print(f"Result: {result.get()}")
else:
    print("Task failed or was revoked.")
