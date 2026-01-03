import random
import time

failure_count = 0
breaker_open = False
latency_seconds = 0.15


def flaky_call():
    time.sleep(latency_seconds)
    if random.random() < 0.35:
        raise TimeoutError("dependency timed out")
    return {"status": "ok", "payload": "fresh data"}


def backoff_for(failures):
    return min(0.2 * (2 ** (failures - 1)), 1.5)


for attempt in range(1, 8):
    if breaker_open:
        print(f"attempt {attempt}: breaker open, skipping request")
        time.sleep(0.5)
        continue

    try:
        response = flaky_call()
        failure_count = 0
        print(f"attempt {attempt}: {response['status']}")
    except TimeoutError as exc:
        failure_count += 1
        print(f"attempt {attempt}: {exc}")
        time.sleep(backoff_for(failure_count))
        if failure_count >= 3:
            breaker_open = True
            print("breaker opened after repeated failures")
