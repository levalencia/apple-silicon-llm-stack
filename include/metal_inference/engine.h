#ifndef METAL_INFERENCE_ENGINE_H
#define METAL_INFERENCE_ENGINE_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define ENGINE_API_VERSION_MAJOR 0
#define ENGINE_API_VERSION_MINOR 1
#define ENGINE_API_VERSION_PATCH 0

typedef struct engine_context* engine_handle_t;

typedef enum {
    ENGINE_OK = 0,
    ENGINE_ERROR_INVALID_ARG = 1,
    ENGINE_ERROR_OUT_OF_MEMORY = 2,
    ENGINE_ERROR_MODEL_INVALID = 3,
    ENGINE_ERROR_DEVICE_NOT_FOUND = 4,
    ENGINE_ERROR_SHADER_COMPILATION = 5,
    ENGINE_ERROR_TENSOR_SHAPE = 6,
} engine_status_t;

typedef struct {
    const char* model_path;
    uint32_t n_threads;
    uint32_t n_gpu_layers;
    uint32_t context_length;
} engine_config_t;

typedef struct {
    const char* token;
    double ttft_ms;
    double tokens_per_sec;
    size_t vram_usage_bytes;
} inference_metric_t;

engine_status_t engine_create(engine_handle_t* ctx, const engine_config_t* config);
void            engine_destroy(engine_handle_t ctx);

engine_status_t engine_eval(engine_handle_t ctx, const int32_t* tokens, size_t n_tokens);
engine_status_t engine_get_logits(engine_handle_t ctx, float** out, size_t* out_count);

const char*     engine_status_string(engine_status_t status);
uint32_t        engine_api_version(void);

#ifdef __cplusplus
}
#endif

#endif
