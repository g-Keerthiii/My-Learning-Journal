# Chaos Engineering for the Local Dev

Date: 2026-03-03
Mood/Energy: Cautiously nervous
Estimated reading time: 6 minutes

## The "Why"
I kept trusting my retry logic like it was a magic spell, and that felt dangerous. I wanted to see what my app would do if the network got slow, a dependency disappeared, or a request took longer than expected. It seemed a lot better to break things on purpose while I still had a terminal open.

## The Exploration
My mental model for chaos engineering changed pretty quickly. I used to think it meant "randomly destroy stuff," but now I think of it more like a fire drill. The point is not the smoke itself. The point is whether people and systems know what to do when the smoke appears.

In my little local setup, I introduced artificial latency and occasional failures so I could watch the app under stress:

- latency showed me whether my timeout values were realistic
- failures showed me whether my retries were respectful or just spammy
- repeated failures showed me whether a circuit breaker should trip instead of letting the request loop forever

The sketch in my head looked like this:

```text
client -> proxy -> service -> database
         ^         |           |
         |         +-- delay ---+
         +-- retry / timeout / breaker
```

What clicked for me was that resilience is not one feature. It is a stack of small decisions: timeout, retry, backoff, fallback, and observability.

## The Code (Crucial)
I wrote a tiny script that simulates a flaky dependency and backs off when failures stack up. The longer version lives in [code/01_chaos_engineering-example.py](../code/01_chaos_engineering-example.py).

```python
import random
import time

failure_count = 0
breaker_open = False


def flaky_call():
    if random.random() < 0.35:
        raise TimeoutError("dependency timed out")
    return "ok"


for attempt in range(1, 8):
    if breaker_open:
        print(f"attempt {attempt}: breaker open, skipping request")
        time.sleep(0.5)
        continue

    try:
        result = flaky_call()
        failure_count = 0
        print(f"attempt {attempt}: {result}")
    except TimeoutError as exc:
        failure_count += 1
        print(f"attempt {attempt}: {exc}")
        time.sleep(0.2 * failure_count)
        if failure_count >= 3:
            breaker_open = True
```

## The "Aha!" Moment
The real shift was realizing that retries are not automatically helpful. If I retry too aggressively, I can make a bad situation worse by piling more work onto something that is already struggling.

## The Struggle
My first attempt looked fine until I realized I had no actual stop condition. I was retrying every failure, but I was not measuring how many failures happened in a row. That made the demo feel fake, because the code never admitted that the dependency was effectively unhealthy. Once I added a failure counter and a breaker state, the behavior finally matched the story I was trying to tell.

## Key Takeaways
- Timeouts are not optional. They define the upper bound of pain.
- Retries need backoff, or they just create more traffic.
- A circuit breaker is useful when failures stop being temporary.
- Chaos testing is more convincing when you make the failure modes specific.
- Resilience is really about choosing where the system should fail gracefully.

## Questions I still have
- How do real systems decide the exact threshold for opening a breaker?
- What is the cleanest way to test chaos experiments without making local dev miserable?
