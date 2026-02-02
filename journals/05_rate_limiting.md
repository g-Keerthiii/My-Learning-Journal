# Sliding Window Rate Limiting in a Proxy

Date: 2026-05-01
Mood/Energy: Annoyed, then satisfied
Estimated reading time: 7 minutes

## The "Why"
I kept seeing rate limiters described as simple, but the implementation details always seemed to hide the actual hard part. I wanted to understand how a proxy could reject traffic fairly without needing an external cache for every decision.

## The Exploration
I started with the idea of a bucket that slowly refills. That was easy enough. The trickier part was the sliding window version, where I wanted the limiter to pay attention to recent request volume instead of just a crude reset at the top of the minute.

My sketch was:

```text
past window  | current window
--------------+----------------
old requests  | new requests
```

The sliding window feels more humane than a strict fixed window. If a user sends a burst right before a clock boundary, a fixed window can accidentally give them a second burst immediately after. The sliding version smooths that edge out.

## The Code (Crucial)
The longer Go example lives in [code/05_rate_limiting-example.go](../code/05_rate_limiting-example.go).

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

type Limiter struct {
    mu       sync.Mutex
    limit    int
    window   time.Duration
    hits     []time.Time
}

func (l *Limiter) Allow(now time.Time) bool {
    l.mu.Lock()
    defer l.mu.Unlock()

    cutoff := now.Add(-l.window)
    kept := l.hits[:0]
    for _, hit := range l.hits {
        if hit.After(cutoff) {
            kept = append(kept, hit)
        }
    }
    l.hits = kept
    if len(l.hits) >= l.limit {
        return false
    }
    l.hits = append(l.hits, now)
    return true
}
```

## The "Aha!" Moment
The main insight was that rate limiting is really a memory problem disguised as a traffic problem. The limiter only works if it remembers the right recent history and forgets old noise quickly enough.

## The Struggle
I got tripped up by off-by-one behavior around the edge of the time window. My first version included events that should have expired, which made the limiter feel randomly strict. Once I compared each request against a cutoff time instead of trying to reason in vague "last minute" terms, the behavior became much easier to trust.

## Key Takeaways
- Fixed windows are easy but can be unfair at the boundary.
- Sliding windows track recent history more smoothly.
- The limiter needs a fast in-memory data structure.
- Time math is where a lot of bugs hide.
- Concurrency matters even when the logic looks simple.

## Questions I still have
- How do large distributed proxies coordinate rate limits without making every request expensive?
- When is a token bucket a better fit than a sliding log?
