# eBPF Tracing for Golang Applications

Date: 2026-06-24
Mood/Energy: Distracted at first, then fascinated
Estimated reading time: 8 minutes

## The "Why"
I wanted to see how people observe a live system without restarting it or adding a pile of new log statements. eBPF looked like the right rabbit hole because it sits close to the kernel but can still be aimed at a specific application.

## The Exploration
The big idea I took away is that eBPF is like a programmable hook system for the Linux kernel. Instead of asking the app to reveal everything, I can attach tiny programs to interesting events such as syscalls, packet handling, or process activity.

My mental model was:

```text
Go app -> kernel event -> eBPF probe -> metrics / trace output
```

That means observability can be added from the outside. I do not need to modify the application just to answer a question about it.

## The Code (Crucial)
The longer Go example lives in [code/11_ebpf_tracing-example.go](../code/11_ebpf_tracing-example.go).

```go
package main

import "fmt"

func main() {
    fmt.Println("load eBPF program")
    fmt.Println("attach to syscall or uprobe")
    fmt.Println("collect latency and drop data")
}
```

## The "Aha!" Moment
The part that clicked was realizing that the kernel can act like a measurement platform, not just a black box. That makes debugging production systems feel much less impossible.

## The Struggle
I spent a while conflating uprobes, kprobes, and tracepoints. They all sound similar when you first read about them, but they attach at different places and answer different questions. Once I grouped them by "where the hook lives," the whole topic got less intimidating.

## Key Takeaways
- eBPF lets me observe behavior from outside the app.
- Probes can attach to kernel or user-space events.
- This is what makes deep production tracing possible.
- The kernel is doing real work as an observability surface.
- The hard part is choosing the right event to hook.

## Questions I still have
- How do tracing tools balance signal quality against overhead?
- What is the cleanest workflow for developing and testing eBPF programs locally?
