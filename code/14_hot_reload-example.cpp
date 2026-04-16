#include <atomic>
#include <filesystem>
#include <iostream>
#include <memory>
#include <string>

struct Config {
    std::string mode;
    bool valid() const { return !mode.empty(); }
};

std::shared_ptr<Config> load_config(const std::string& path) {
    auto config = std::make_shared<Config>();
    config->mode = std::filesystem::exists(path) ? "production" : "fallback";
    return config;
}

int main() {
    std::atomic<std::shared_ptr<Config>> current{load_config("app.yml")};
    auto next = load_config("app.yml");
    if (next->valid()) {
        current.store(next);
    }
    std::cout << current.load()->mode << std::endl;
}
