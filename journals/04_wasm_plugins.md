# Server-Side WebAssembly Plugins

Date: 2026-04-16
Mood/Energy: Curious and a little skeptical
Estimated reading time: 6 minutes

## The "Why"
I wanted to understand why people keep saying WebAssembly is a good plugin format. The claim sounded a little too neat: write untrusted code, run it safely, keep performance decent. I needed to see where the safety boundary actually lives.

## The Exploration
My simplified mental model is that WebAssembly is a locked room with a strict door policy. The host application decides what the guest is allowed to call, and the guest module only gets the capabilities I hand it. That is much different from loading a script and hoping it behaves.

What helped was thinking in terms of a contract:

- the host provides functions like logging or storage
- the plugin exports a small set of predictable entry points
- memory is isolated unless I explicitly expose something

So instead of "run arbitrary code," it feels more like "run code inside a box with a few approved tools." That made the security story much less mystical.

## The Code (Crucial)
The longer Rust example lives in [code/04_wasm_plugins-example.rs](../code/04_wasm_plugins-example.rs).

```rust
trait HostApi {
    fn log(&self, message: &str);
}

struct Runner;

impl HostApi for Runner {
    fn log(&self, message: &str) {
        println!("plugin: {}", message);
    }
}

fn invoke_plugin(api: &dyn HostApi, input: i32) -> i32 {
    api.log("running wasm plugin");
    input * 2 + 1
}
```

## The "Aha!" Moment
The biggest realization was that the host does not need to trust the plugin. It just needs to be explicit about the tiny surface area it exposes. That is a much better fit for extensions than embedding a huge scripting runtime.

## The Struggle
I initially mixed up isolation with performance. I assumed "sandboxed" had to mean "slow," but the point of WASM is that it keeps the sandbox boundary tight without forcing me into a heavyweight interpreter. I also kept overthinking memory sharing. Once I accepted that shared state should be intentional and narrow, the architecture became much cleaner.

## Key Takeaways
- WASM plugins are capability-based, not ambient-access-based.
- The host decides what the guest can touch.
- Isolation is part of the design, not an afterthought.
- Good plugin APIs stay tiny and explicit.
- The box is useful because it is hard to escape.

## Questions I still have
- What is the best pattern for versioning plugin interfaces without breaking old modules?
- When does a native extension beat WASM in a real production workload?
