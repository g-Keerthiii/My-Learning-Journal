# Hot-Reloading Configs using Inotify

Date: 2026-07-15
Mood/Energy: Impatient, then calmer
Estimated reading time: 7 minutes

## The "Why"
I was tired of restarting services every time I changed a configuration file. That workflow is fine for a toy app, but it gets old fast when the service is long-running and stateful.

## The Exploration
The main thing I learned is that hot reloading is mostly a state-management problem. Watching the file is the easy part. The hard part is loading the new config safely, validating it, and swapping it into memory without exposing half-written state to the live request path.

My rough sketch was:

```text
file change -> reload config -> validate -> atomic swap -> serve requests
```

Once I thought about it that way, inotify felt like just the trigger, not the whole solution.

## The Code (Crucial)
The longer C++ example lives in [code/14_hot_reload-example.cpp](../code/14_hot_reload-example.cpp).

```cpp
if (event.mask & IN_CLOSE_WRITE) {
    auto next = load_config(path);
    if (next.valid()) {
        current.store(next);
    }
}
```

## The "Aha!" Moment
The click was realizing that the reload path and the request path should barely know about each other. The reload thread prepares a new config object, and the live server just swaps a pointer when it is safe.

## The Struggle
I first tried mutating the existing config object in place, which was a bad idea because it created a tiny race window. That made the behavior feel flaky and hard to reason about. Once I switched to building a fresh config and swapping it atomically, the whole feature felt much safer.

## Key Takeaways
- Watching files is only the trigger for hot reload.
- Validation needs to happen before the swap.
- Immutable replacement is safer than in-place mutation.
- inotify is useful, but it is not the whole design.
- The live request path should stay simple.

## Questions I still have
- How do production systems debounce noisy file change events cleanly?
- What is the safest way to roll back a bad config after it has already been loaded?
