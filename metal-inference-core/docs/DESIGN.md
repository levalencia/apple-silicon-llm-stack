# Metal Inference Core - Design Patterns & SOLID Principles

## Design Patterns

### 1. RAII (Resource Acquisition Is Initialization)

Ensures automatic resource cleanup:

```cpp
class Buffer {
public:
    explicit Buffer(MTLDevice* device, size_t size)
        : device_(device), size_(size) {
        buffer_ = [device_ newBufferWithLength:size
                   options:MTLResourceStorageModeShared];
    }
    
    ~Buffer() {
        // Automatically released when goes out of scope
    }
    
private:
    MTLDevice* device_;
    id<MTLBuffer> buffer_;
    size_t size_;
};
```

**Usage**:
```cpp
void process() {
    Buffer temp_buffer(device, 1024);
    // Use buffer
} // Automatically cleaned up here
```

### 2. PImpl (Pointer to Implementation)

Hides implementation details:

```cpp
// engine.h - Public header
class Engine {
public:
    Engine();
    ~Engine();
    
    InferenceResult infer(const InferenceRequest& req);
    
private:
    class Impl;  // Forward declaration
    std::unique_ptr<Impl> impl_;
};

// engine.cpp - Implementation
class Engine::Impl {
public:
    void initDevice() { /* ... */ }
    void loadModel() { /* ... */ }
    // Private implementation details
};
```

### 3. Factory Pattern

For creating platform-specific objects:

```cpp
class DeviceFactory {
public:
    static std::unique_ptr<MetalDevice> create() {
        auto device = MTLCreateSystemDefaultDevice();
        if (!device) {
            return nullptr;
        }
        return std::make_unique<MetalDevice>(device);
    }
};
```

### 4. Strategy Pattern

For swappable sampling strategies:

```cpp
class ISampler {
public:
    virtual ~ISampler() = default;
    virtual Token sample(const Tensor& logits) = 0;
};

class GreedySampler : public ISampler {
    Token sample(const Tensor& logits) override;
};

class TopKSampler : public ISampler {
    Token sample(const Tensor& logits) override;
};

class Sampler {
public:
    void setStrategy(std::unique_ptr<ISampler> strategy) {
        strategy_ = std::move(strategy);
    }
    
    Token sample(const Tensor& logits) {
        return strategy_->sample(logits);
    }
    
private:
    std::unique_ptr<ISampler> strategy_;
};
```

### 5. Object Pool

For reusing GPU buffers:

```cpp
class BufferPool {
public:
    BufferPool(MTLDevice* device) : device_(device) {}
    
    id<MTLBuffer> acquire(size_t size) {
        auto key = normalize_size(size);
        if (auto it = pool_.find(key); it != pool_.end() && !it->second.empty()) {
            auto buffer = it->second.front();
            it->second.pop_front();
            return buffer;
        }
        return [device_ newBufferWithLength:key 
                options:MTLResourceStorageModeShared];
    }
    
    void release(id<MTLBuffer> buffer) {
        auto size = [buffer length];
        pool_[size].push_back(buffer);
    }
    
private:
    MTLDevice* device_;
    std::unordered_map<size_t, std::deque<id<MTLBuffer>>> pool_;
};
```

### 6. Builder Pattern

For complex configuration:

```cpp
class EngineBuilder {
public:
    EngineBuilder& model_path(std::string path) {
        config_.model_path = std::move(path);
        return *this;
    }
    
    EngineBuilder& gpu_layers(uint32_t layers) {
        config_.n_gpu_layers = layers;
        return *this;
    }
    
    EngineBuilder& context_length(uint32_t len) {
        config_.context_length = len;
        return *this;
    }
    
    std::expected<std::unique_ptr<Engine>, Error> build() {
        if (config_.model_path.empty()) {
            return std::unexpected(Error::InvalidModel);
        }
        return std::make_unique<Engine>(config_);
    }
    
private:
    InferenceConfig config_;
};

// Usage
auto engine = EngineBuilder()
    .model_path("./model.gguf")
    .gpu_layers(32)
    .context_length(2048)
    .build();
```

## SOLID Principles

### Single Responsibility

| File | Class | Responsibility |
|------|-------|---------------|
| `model_loader.cpp` | `ModelLoader` | GGUF parsing |
| `engine.cpp` | `Engine` | Inference orchestration |
| `sampler.cpp` | `Sampler` | Token selection |
| `device.mm` | `MetalDevice` | GPU management |
| `buffer_pool.mm` | `BufferPool` | Memory allocation |

### Open/Closed

Extending without modification:

```cpp
// Add new quantization without changing loader
class IQuantizer {
public:
    virtual ~IQuantizer() = default;
    virtual Tensor dequantize(const QuantizedTensor& input) = 0;
};

class Q4Quantizer : public IQuantizer { /* ... */ };
class Q5Quantizer : public IQuantizer { /* ... */ };
class Q6Quantizer : public IQuantizer { /* ... */ };
class Q8Quantizer : public IQuantizer { /* ... */ };

// New quantization can be added without modifying existing code
```

### Liskov Substitution

Any implementation works:

```cpp
void processBuffer(IDevice* device) {
    auto buf = device->allocate(1024);
    // Works with MetalDevice, or mock for testing
}

processBuffer(&realDevice);  // Production
processBuffer(&mockDevice); // Testing
```

### Interface Segregation

Small, focused interfaces:

```cpp
// ❌ Large interface
class ILargeDevice {
public:
    virtual void allocate() = 0;
    virtual void copy() = 0;
    virtual void submit() = 0;
    virtual void wait() = 0;
};

// ✅ Focused interfaces
class IAllocator {
public:
    virtual Buffer* allocate(size_t) = 0;
};

class ICommandSubmitter {
public:
    virtual void submit(CommandBuffer&) = 0;
    virtual void wait() = 0;
};
```

### Dependency Inversion

```cpp
// ❌ High-level depends on low-level
class Engine {
    MetalDevice device_;  // Depends on concrete
};

// ✅ Depends on abstraction
class Engine {
    std::unique_ptr<IDevice> device_;  // Interface
};
```

## RAII in Practice

### Scoped Timers

```cpp
class ScopedTimer {
public:
    ScopedTimer(const char* name, Logger& logger)
        : name_(name), logger_(logger), start_(std::chrono::steady_clock::now()) {}
    
    ~ScopedTimer() {
        auto elapsed = std::chrono::steady_clock::now() - start_;
        logger_.info("{} took {}ms", name_, 
            std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count());
    }
    
private:
    const char* name_;
    Logger& logger_;
    std::chrono::time_point<std::chrono::steady_clock> start_;
};

// Usage
void inference() {
    ScopedTimer timer("inference", logger_);
    // Inference logic
} // Timer reports duration automatically
```

### Lock Guards

```cpp
class ThreadSafeQueue {
public:
    void push(Item item) {
        std::lock_guard<std::mutex> lock(mutex_);
        queue_.push(std::move(item));
    }
    
private:
    std::mutex mutex_;
    std::queue<Item> queue_;
};
```

## Error Handling

### Result Type

```cpp
template<typename T>
class Result {
public:
    bool ok() const { return value_.has_value(); }
    T& value() { return value_.value(); }
    Error error() const { return error_.value(); }
    
    static Result success(T value) {
        Result r;
        r.value_ = std::move(value);
        return r;
    }
    
    static Result failure(Error err) {
        Result r;
        r.error_ = err;
        return r;
    }
    
private:
    std::optional<T> value_;
    std::optional<Error> error_;
};
```

### Usage

```cpp
Result<Tensor> loadTensor(const std::string& path) {
    if (!file_exists(path)) {
        return Result<Tensor>::failure(Error::InvalidModel);
    }
    
    auto data = read_file(path);
    if (data.size() == 0) {
        return Result<Tensor>::failure(Error::InvalidModel);
    }
    
    return Result<Tensor>::success(Tensor(data));
}
```
