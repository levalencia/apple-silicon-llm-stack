#include <iostream>
#include <cassert>
#include <cmath>
#include "metal_inference/types.h"

namespace metal_inference {
namespace tests {

void test_float_to_uint8() {
    float input = 0.5f;
    uint8_t result = float_to_uint8(input, 0.0f, 1.0f);
    assert(result >= 0 && result <= 255);
    std::cout << "test_float_to_uint8 PASSED: " << (int)result << std::endl;
}

void test_uint8_to_float() {
    uint8_t input = 128;
    float result = uint8_to_float(input, 0.0f, 1.0f);
    assert(std::abs(result - 0.5f) < 0.01f);
    std::cout << "test_uint8_to_float PASSED: " << result << std::endl;
}

void test_roundtrip() {
    float original = 0.785f;
    uint8_t quantized = float_to_uint8(original, 0.0f, 1.0f);
    float restored = uint8_to_float(quantized, 0.0f, 1.0f);
    assert(std::abs(original - restored) < 0.02f);
    std::cout << "test_roundtrip PASSED: " << original << " -> " << (int)quantized << " -> " << restored << std::endl;
}

void test_clamp() {
    float neg = float_to_uint8(-0.5f, 0.0f, 1.0f);
    assert(neg == 0);
    float pos = float_to_uint8(1.5f, 0.0f, 1.0f);
    assert(pos == 255);
    std::cout << "test_clamp PASSED" << std::endl;
}

void test_tensor_create() {
    Tensor t({2, 3}, DataType::Float32);
    assert(t.shape()[0] == 2);
    assert(t.shape()[1] == 3);
    assert(t.dtype() == DataType::Float32);
    std::cout << "test_tensor_create PASSED" << std::endl;
}

void test_tensor_size() {
    Tensor t({2, 3, 4}, DataType::Float32);
    assert(t.size() == 24);
    std::cout << "test_tensor_size PASSED: " << t.size() << std::endl;
}

void test_tensor_bytes() {
    Tensor t({2, 3}, DataType::Float32);
    assert(t.bytes() == 24);
    std::cout << "test_tensor_bytes PASSED: " << t.bytes() << std::endl;
}

}
}

int main() {
    std::cout << "Running metal-inference-core unit tests..." << std::endl;
    
    metal_inference::tests::test_float_to_uint8();
    metal_inference::tests::test_uint8_to_float();
    metal_inference::tests::test_roundtrip();
    metal_inference::tests::test_clamp();
    metal_inference::tests::test_tensor_create();
    metal_inference::tests::test_tensor_size();
    metal_inference::tests::test_tensor_bytes();
    
    std::cout << "\nAll tests PASSED!" << std::endl;
    return 0;
}
