package main

import (
    "fmt"
    "sync"
    "time"
)

type Limiter struct {
    mu     sync.Mutex
    limit  int
    window time.Duration
    hits   []time.Time
}

func NewLimiter(limit int, window time.Duration) *Limiter {
    return &Limiter{limit: limit, window: window}
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

func main() {
    limiter := NewLimiter(3, 10*time.Second)
    now := time.Now()
    for i := 0; i < 5; i++ {
        allowed := limiter.Allow(now.Add(time.Duration(i) * time.Second))
        fmt.Println(i, allowed)
    }
}
