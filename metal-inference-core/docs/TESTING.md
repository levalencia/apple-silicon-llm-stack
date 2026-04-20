# Metal Inference Core - Testing Guide

## Test Overview

| Category | Count | Location |
|----------|-------|----------|
| Unit Tests | 7 | `tests/unit/main.cpp` |
| Test Framework | Custom | Assertion-based |

## Running Tests

### Quick Run

```bash
cd /Users/luisvalencia/Documents/metal-inference-core/build
ctest
```

### Verbose Output

```bash
ctest --output-on-failure -V
```

### Run Binary Directly

```bash
./build/bin/unit_tests
```

## Test Structure

```
tests/
├── CMakeLists.txt          # Test build configuration
├── unit/
│   └── main.cpp            # Unit tests (7 tests)
└── integration/
    └── (placeholder)
```

## Test Descriptions

### Unit Tests (`tests/unit/main.cpp`)

| Test | Description |
|------|-------------|
| `test_float_to_uint8` | Quantize float to uint8 |
| `test_uint8_to_float` | Dequantize uint8 to float |
| `test_roundtrip` | FP16 → Q4 → FP16 |
| `test_clamp` | Boundary clamping |
| `test_tensor_create` | Tensor construction |
| `test_tensor_size` | Tensor size calculation |
| `test_tensor_bytes` | Byte size calculation |

## Writing Tests

### Basic Test Structure

```cpp
#include <iostream>
#include <cassert>
#include "metal_inference/types.h"

void test_example() {
    // Arrange
    int input = 5;
    
    // Act
    int result = input * 2;
    
    // Assert
    assert(result == 10);
    std::cout << "test_example PASSED" << std::endl;
}

int main() {
    test_example();
    return 0;
}
```

### Test with Floating Point

```cpp
void test_float_comparison() {
    float expected = 0.5f;
    float actual = compute_value();
    
    // Use tolerance for floats
    assert(std::abs(expected - actual) < 0.001f);
}
```

### Test Tensor Operations

```cpp
void test_tensor_operations() {
    Tensor t({2, 3}, DataType::Float32);
    
    // Verify shape
    assert(t.shape()[0] == 2);
    assert(t.shape()[1] == 3);
    
    // Verify size
    assert(t.size() == 6);
    
    // Verify bytes
    assert(t.bytes() == 24); // 6 * 4 bytes
}
```

## Building Tests

### Debug Build with Tests

```bash
cd /Users/luisvalencia/Documents/metal-inference-core
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Debug -DENABLE_TESTING=ON
make -j4
```

### Run Tests

```bash
ctest --output-on-failure
```

## Test Coverage

Current unit tests cover:

- **Quantization**: Float ↔ Uint8 conversion, clamping, roundtrip
- **Tensor**: Creation, size, bytes calculation

### Adding More Tests

1. Add test function to `tests/unit/main.cpp`:

```cpp
void test_my_feature() {
    // Test implementation
    assert(condition);
    std::cout << "test_my_feature PASSED" << std::endl;
}
```

2. Add to `main()`:

```cpp
int main() {
    test_float_to_uint8();
    test_uint8_to_float();
    // ... existing tests
    test_my_feature();  // Add here
    
    std::cout << "\nAll tests PASSED!" << std::endl;
    return 0;
}
```

3. Rebuild:

```bash
make -j4
./bin/unit_tests
```

## Integration Testing

### Manual Integration Test

```bash
# Build CLI
./build/bin/inference_cli \
    --model /path/to/model.gguf \
    --prompt "The capital of France is"
```

Expected output:
- Generated text completion
- Timing metrics

## Benchmarking

### Build Benchmark

```bash
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j4
```

### Run Benchmarks

```bash
make bench
```

Or manually:

```bash
./build/bin/inference_cli \
    --model model.gguf \
    --prompt "Write a story about" \
    --max_tokens 100
```

## Debugging

### With lldb

```bash
lldb ./build/bin/unit_tests
(lldb) run
```

### With Address Sanitizer

```bash
cmake .. -DCMAKE_BUILD_TYPE=Debug \
    -DENABLE_SANITIZERS=ON \
    -DCMAKE_CXX_FLAGS="-fsanitize=address"
make -j4
./bin/unit_tests
```

### With Thread Sanitizer

```bash
cmake .. -DCMAKE_BUILD_TYPE=Debug \
    -DENABLE_SANITIZERS=ON \
    -DCMAKE_CXX_FLAGS="-fsanitize=thread"
make -j4
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: macos-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build
        run: |
          mkdir build
          cd build
          cmake .. -DCMAKE_BUILD_TYPE=Debug
          make -j4
      
      - name: Test
        run: |
          cd build
          ctest --output-on-failure
```
