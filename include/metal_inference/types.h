#include <vector>
#include <cstdint>
#include <cmath>
#include <algorithm>

namespace metal_inference {

enum class Error : uint32_t {
    Ok = 0,
    InvalidModel,
    OutOfMemory,
    MetalDeviceNotFound,
    ShaderCompilationFailed,
    InvalidTensorShape,
};

enum class QuantizationType : uint32_t {
    None = 0,
    Q4_K_M,
    Q5_K_M,
    Q6_K,
    Q8_0,
};

struct InferenceConfig {
    std::string model_path;
    uint32_t n_threads = 4;
    uint32_t n_gpu_layers = 32;
    uint32_t context_length = 2048;
};

struct InferenceMetric {
    std::string token;
    double ttft_ms = 0.0;
    double tokens_per_sec = 0.0;
    size_t vram_usage_bytes = 0;
};

struct InferenceResult {
    std::vector<float> logits;
    InferenceMetric metric;
};

enum class DataType : uint32_t {
    Float32 = 0,
    Float16,
    Int8,
    UInt8,
};

class Tensor {
public:
    Tensor(const std::vector<uint32_t>& shape, DataType dtype)
        : shape_(shape), dtype_(dtype), data_(1, 0.0f) {
        size_ = 1;
        for (auto dim : shape_) size_ *= dim;
        data_.resize(size_);
    }

    const std::vector<uint32_t>& shape() const { return shape_; }
    DataType dtype() const { return dtype_; }
    size_t size() const { return size_; }
    size_t bytes() const { 
        switch (dtype_) {
            case DataType::Float32: return size_ * 4;
            case DataType::Float16: return size_ * 2;
            case DataType::Int8: case DataType::UInt8: return size_;
            default: return size_ * 4;
        }
    }
    float* data() { return data_.data(); }
    const float* data() const { return data_.data(); }

private:
    std::vector<uint32_t> shape_;
    DataType dtype_;
    size_t size_;
    std::vector<float> data_;
};

inline uint8_t float_to_uint8(float value, float min_val, float max_val) {
    float normalized = (value - min_val) / (max_val - min_val);
    normalized = std::max(0.0f, std::min(1.0f, normalized));
    return static_cast<uint8_t>(std::round(normalized * 255.0f));
}

inline float uint8_to_float(uint8_t value, float min_val, float max_val) {
    return min_val + (static_cast<float>(value) / 255.0f) * (max_val - min_val);
}

}
