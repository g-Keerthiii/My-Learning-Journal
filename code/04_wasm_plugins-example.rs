trait HostApi {
    fn log(&self, message: &str);
}

struct Runner;

impl HostApi for Runner {
    fn log(&self, message: &str) {
        println!("plugin: {}", message);
    }
}

struct PluginInput {
    value: i32,
}

fn invoke_plugin(api: &dyn HostApi, input: PluginInput) -> i32 {
    api.log("loading plugin module");
    let transformed = input.value * 2 + 1;
    api.log(&format!("plugin returned {}", transformed));
    transformed
}

fn main() {
    let runner = Runner;
    let output = invoke_plugin(&runner, PluginInput { value: 21 });
    println!("final output: {}", output);
}
