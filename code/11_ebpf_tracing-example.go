package main

import "fmt"

func loadProgram() {
    fmt.Println("loading eBPF bytecode")
}

func attachProbe(target string) {
    fmt.Println("attaching probe to", target)
}

func collectMetrics() {
    fmt.Println("collecting syscall latency and packet drop metrics")
}

func main() {
    loadProgram()
    attachProbe("sys_enter_write")
    attachProbe("tcp_sendmsg")
    collectMetrics()
}
