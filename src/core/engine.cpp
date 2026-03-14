#include "metal_inference/engine.h"
#include "metal_inference/types.h"
#include <memory>
#include <spdlog/spdlog.h>
#include <string>

namespace metal_inference {

class InferenceEngine {
public:
    static std::unique_ptr<InferenceEngine> create(const InferenceConfig& config) {
        spdlog::info("Creating inference engine");
        
        if (config.model_path.empty()) {
            return nullptr;
        }
        
        return std::unique_ptr<InferenceEngine>(new InferenceEngine(config));
    }
    
    ~InferenceEngine() = default;
    
    void load_model(const std::string& path) {
        spdlog::info("Loading model from {}", path);
    }
    
    InferenceResult eval(const std::vector<int32_t>& tokens) {
        spdlog::debug("Evaluating {} tokens", tokens.size());
        
        InferenceResult result;
        result.logits.resize(32000);
        result.metric.tokens_per_sec = 100.0;
        result.metric.ttft_ms = 50.0;
        
        return result;
    }
    
    size_t get_vram_usage() const {
        return vram_usage_;
    }
    
private:
    explicit InferenceEngine(const InferenceConfig& config) 
        : config_(config), vram_usage_(0) {}
    
    InferenceConfig config_;
    size_t vram_usage_;
};

}

extern "C" {

engine_status_t engine_create(engine_handle_t* ctx, const engine_config_t* config) {
    if (!ctx || !config) {
        return ENGINE_ERROR_INVALID_ARG;
    }
    
    metal_inference::InferenceConfig cfg;
    cfg.model_path = config->model_path ? config->model_path : "";
    cfg.n_threads = config->n_threads;
    cfg.n_gpu_layers = config->n_gpu_layers;
    cfg.context_length = config->context_length;
    
    auto engine = metal_inference::InferenceEngine::create(cfg);
    
    if (!engine) {
        return ENGINE_ERROR_OUT_OF_MEMORY;
    }
    
    *ctx = reinterpret_cast<engine_context*>(engine.release());
    return ENGINE_OK;
}

void engine_destroy(engine_handle_t ctx) {
    if (ctx) {
        delete reinterpret_cast<metal_inference::InferenceEngine*>(ctx);
    }
}

engine_status_t engine_eval(engine_handle_t ctx, const int32_t* tokens, size_t n_tokens) {
    if (!ctx || !tokens || n_tokens == 0) {
        return ENGINE_ERROR_INVALID_ARG;
    }
    
    auto* engine = reinterpret_cast<metal_inference::InferenceEngine*>(ctx);
    std::vector<int32_t> token_vec(tokens, tokens + n_tokens);
    engine->eval(token_vec);
    
    return ENGINE_OK;
}

const char* engine_status_string(engine_status_t status) {
    switch (status) {
        case ENGINE_OK: return "OK";
        case ENGINE_ERROR_INVALID_ARG: return "Invalid argument";
        case ENGINE_ERROR_OUT_OF_MEMORY: return "Out of memory";
        case ENGINE_ERROR_MODEL_INVALID: return "Invalid model";
        case ENGINE_ERROR_DEVICE_NOT_FOUND: return "Device not found";
        case ENGINE_ERROR_SHADER_COMPILATION: return "Shader compilation failed";
        case ENGINE_ERROR_TENSOR_SHAPE: return "Invalid tensor shape";
        default: return "Unknown error";
    }
}

uint32_t engine_api_version(void) {
    return (ENGINE_API_VERSION_MAJOR << 16) | 
           (ENGINE_API_VERSION_MINOR << 8) | 
           ENGINE_API_VERSION_PATCH;
}
}
