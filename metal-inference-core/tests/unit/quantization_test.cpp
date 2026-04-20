#include <gtest/gtest.h>
#include "metal_inference/types.h"
#include <cmath>

namespace metal_inference {
namespace tests {

class QuantizationTest : public ::testing::Test {
protected:
    void SetUp() override {}
};

TEST_F(QuantizationTest, FloatToUint8) {
    float input = 0.5f;
    uint8_t result = float_to_uint8(input, 0.0f, 1.0f);
    EXPECT_GE(result, 0);
    EXPECT_LE(result, 255);
}

TEST_F(QuantizationTest, Uint8ToFloat) {
    uint8_t input = 128;
    float result = uint8_to_float(input, 0.0f, 1.0f);
    EXPECT_NEAR(result, 0.5f, 0.01f);
}

TEST_F(QuantizationTest, RoundTrip) {
    float original = 0.785f;
    uint8_t quantized = float_to_uint8(original, 0.0f, 1.0f);
    float restored = uint8_to_float(quantized, 0.0f, 1.0f);
    EXPECT_NEAR(original, restored, 0.02f);
}

TEST_F(QuantizationTest, ClampMin) {
    float input = -0.5f;
    uint8_t result = float_to_uint8(input, 0.0f, 1.0f);
    EXPECT_EQ(result, 0);
}

TEST_F(QuantizationTest, ClampMax) {
    float input = 1.5f;
    uint8_t result = float_to_uint8(input, 0.0f, 1.0f);
    EXPECT_EQ(result, 255);
}

class TensorTest : public ::testing::Test {
protected:
    void SetUp() override {}
};

TEST_F(TensorTest, CreateTensor) {
    Tensor t({2, 3}, DataType::Float32);
    EXPECT_EQ(t.shape()[0], 2);
    EXPECT_EQ(t.shape()[1], 3);
    EXPECT_EQ(t.dtype(), DataType::Float32);
}

TEST_F(TensorTest, TensorSize) {
    Tensor t({2, 3, 4}, DataType::Float32);
    EXPECT_EQ(t.size(), 24);
}

TEST_F(TensorTest, TensorBytes) {
    Tensor t({2, 3}, DataType::Float32);
    EXPECT_EQ(t.bytes(), 24);
}

}  
}  

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
