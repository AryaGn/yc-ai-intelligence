# worker.py
import time
from tasks import get_pending_tasks, complete_task, fail_task
from llm import analyze_company

while True:
    tasks = get_pending_tasks()

    for task in tasks:
        try:
            result = analyze_company(task["input_payload"])
            complete_task(task["id"], result)
        except Exception as e:
            fail_task(task["id"], str(e))

    time.sleep(10)