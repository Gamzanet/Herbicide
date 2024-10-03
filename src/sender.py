# src/app.py

from task.tasks import analysis  # task 패키지에서 add 작업 가져오기

# 작업 호출 (비동기)
result = analysis.delay(4, 6)

# 작업 ID 출력
print(f"Task ID: {result.id}")

# 작업 상태를 계속 조회
while not result.ready():
    print(f"Task Status: {result.status}")

# 결과 확인
if result.successful():
    print(f"Task Status: {result.status}")
    print(f"Result: {result.get()}")
else:
    print("Task failed or was revoked.")
