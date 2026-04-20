# Architecture Decision Records - Metal Inference Core

## ADR-001: Use C++20 with Apple Clang

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need modern C++ features for:
- Concepts for generic programming
- std::expected for error handling
- std::span for bounds-safe views
- Structured bindings

### Decision

Use C++20 with Apple Clang 17.

### Consequences

**Positive**:
- Modern language features
- Better type safety
- Improved ergonomics

**Negative**:
- Some C++23 features unavailable (std::expected not fully supported)
- Workaround: use custom Result type

---

## ADR-002: Use Metal for GPU Acceleration

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need GPU acceleration for:
- Matrix multiplication
- KV cache management
- Quantization kernels

### Decision

Use Apple Metal framework:

```cpp
id<MTLDevice> device = MTLCreateSystemDefaultDevice();
id<MTLCommandQueue> queue = [device newCommandQueue];
```

### Consequences

**Positive**:
- Native Apple Silicon support
- Zero-copy memory when possible
- High performance

**Negative**:
- macOS only
- Requires Metal knowledge

---

## ADR-003: Use RAII for Resource Management

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need automatic resource cleanup for:
- Metal buffers
- Command buffers
- Shader libraries

### Decision

Wrap resources in RAII classes:

```cpp
class Buffer {
public:
    explicit Buffer(MTLDevice* device, size_t size) {
        buffer_ = [device newBufferWithLength:size
                   options:MTLResourceStorageModeShared];
    }
    
    ~Buffer() {
        // Automatic cleanup
    }
};
```

### Consequences

**Positive**:
- No memory leaks
- Exception safe
- Clear ownership

---

## ADR-004: Custom Test Framework

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need lightweight testing without heavy dependencies:
- Catch2 adds build complexity
- Google Test is heavy
- Simple assertion-based tests sufficient

### Decision

Use custom minimal test framework:

```cpp
void test_name() {
    assert(condition);
    std::cout << "test_name PASSED" << std::endl;
}
```

### Consequences

**Positive**:
- No external dependencies
- Fast to build
- Simple to extend

**Negative**:
- Less features than Catch2
- No parameterized tests

---

## ADR-005: Support Multiple Quantization Types

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need to balance model size vs. quality:
- Q4_K_M: Best size/quality ratio
- Q5_K_M: Better quality
- Q6_K: High quality
- Q8_0: Highest quality

### Decision

Support all four formats with pluggable quantizers:

```cpp
enum class QuantizationType : uint32_t {
    None = 0,
    Q4_K_M,
    Q5_K_M,
    Q6_K,
    Q8_0,
};
```

### Consequences

**Positive**:
- Flexibility for different use cases
- Industry standard formats

**Negative**:
- More code to maintain

---

## ADR-006: Use CMake for Build

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need cross-platform build system:
- Xcode is macOS only
- Make is too simple
- Good Metal support in CMake

### Decision

Use CMake with FetchContent for dependencies:

```cmake
FetchContent_Declare(spdlog
    GIT_REPOSITORY https://github.com/gabime/spdlog.git
    GIT_TAG v1.15.0
    FIND_PACKAGE_ARGS
)
FetchContent_MakeAvailable(spdlog)
```

### Consequences

**Positive**:
- Cross-platform
- Good IDE integration
- Easy dependency management

---

## ADR-007: PImpl for ABI Stability

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need stable C-API for Go bindings:
- Changing internal classes breaks ABI
- Need forward declaration

### Decision

Use PImpl pattern:

```cpp
class Engine {
public:
    // Public API
private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};
```

### Consequences

**Positive**:
- Stable ABI
- Faster compile times
- Hide implementation

---

## ADR-008: SPDlog for Logging

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need structured logging:
- printf is too basic
- iostream is slow
- SPDlog is header-only, fast

### Decision

Use SPDlog:

```cpp
#include <spdlog/spdlog.h>
spdlog::info("Model loaded: {}", model_name);
```

### Consequences

**Positive**:
- Fast, async logging
- Multiple sinks
- Good formatting
