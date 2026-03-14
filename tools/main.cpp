#include <iostream>
#include <string>
#include <cstring>

extern "C" {
#include "metal_inference/engine.h"
}

void print_usage(const char* prog) {
    std::cout << "Usage: " << prog << " <command> [options]\n";
    std::cout << "Commands:\n";
    std::cout << "  bench <model.gguf>  Run benchmark\n";
    std::cout << "  info <model.gguf>   Show model info\n";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }
    
    std::string cmd = argv[1];
    
    if (cmd == "bench") {
        if (argc < 3) {
            std::cerr << "Error: model path required\n";
            return 1;
        }
        
        engine_config_t config = {};
        config.model_path = argv[2];
        config.n_threads = 4;
        config.n_gpu_layers = 32;
        config.context_length = 2048;
        
        engine_handle_t ctx = nullptr;
        engine_status_t status = engine_create(&ctx, &config);
        
        if (status != ENGINE_OK) {
            std::cerr << "Error: " << engine_status_string(status) << "\n";
            return 1;
        }
        
        std::cout << "Running benchmark...\n";
        
        engine_destroy(ctx);
        std::cout << "Done\n";
    } else if (cmd == "info") {
        if (argc < 3) {
            std::cerr << "Error: model path required\n";
            return 1;
        }
        
        std::cout << "Model: " << argv[2] << "\n";
        std::cout << "API Version: " << engine_api_version() << "\n";
    } else {
        std::cerr << "Unknown command: " << cmd << "\n";
        print_usage(argv[0]);
        return 1;
    }
    
    return 0;
}
