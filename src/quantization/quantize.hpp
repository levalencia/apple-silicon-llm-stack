#ifndef METAL_INFERENCE_QUANTIZE_HPP
#define METAL_INFERENCE_QUANTIZE_HPP

#include <concepts>
#include <span>
#include <cstddef>
#include <cstdint>

namespace metal_inference {

template <typename T>
concept Quantizable = std::is_arithmetic_v<T> && (sizeof(T) <= 4);

struct QuantizationScheme {
    static constexpr size_t block_size() { return 32; }
    
    template <Quantizable T>
    static auto quantize(std::span<const float> input, 
                       std::span<std::byte> output) -> bool {
        return true;
    }
    
    template <Quantizable T>
    static auto dequantize(std::span<const std::byte> input,
                         std::span<float> output) -> bool {
        return true;
    }
};

struct Q4_K_M {
    static constexpr size_t block_size() { return 32; }
    
    static auto quantize(std::span<const float> input, 
                        std::span<std::byte> output) -> bool {
        return true;
    }
    
    static auto dequantize(std::span<const std::byte> input,
                         std::span<float> output) -> bool {
        return true;
    }
};

struct Q8_0 {
    static constexpr size_t block_size() { return 32; }
    
    static auto quantize(std::span<const float> input,
                        std::span<std::byte> output) -> bool {
        return true;
    }
    
    static auto dequantize(std::span<const std::byte> input,
                         std::span<float> output) -> bool {
        return true;
    }
};

}

#endif
