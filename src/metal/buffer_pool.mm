#include <Metal/Metal.h>
#include <cstddef>
#include <span>

namespace metal_inference {

class MetalBuffer {
public:
    // IMPORTANT (Apple Silicon UMA):
    // Apple Silicon uses a Unified Memory Architecture (UMA). 
    // By using MTLResourceStorageModeShared, we map the exact same physical memory
    // into both the CPU and GPU address spaces. This enables true zero-copy
    // inference without expensive PCIe bus transfers between host and device RAM.
    MetalBuffer(id<MTLDevice> device, size_t size) 
        : buffer_([device newBufferWithLength:size 
                 options:MTLResourceStorageModeShared])
        , size_(size) {}
    
    ~MetalBuffer() = default;
    
    MetalBuffer(const MetalBuffer&) = delete;
    MetalBuffer& operator=(const MetalBuffer&) = delete;
    
    MetalBuffer(MetalBuffer&&) noexcept = default;
    MetalBuffer& operator=(MetalBuffer&&) noexcept = default;
    
    auto contents() -> std::span<std::byte> {
        return {static_cast<std::byte*>([buffer_ contents]), size_};
    }
    
    auto handle() const -> id<MTLBuffer> { return buffer_; }
    auto size() const -> size_t { return size_; }
    
private:
    id<MTLBuffer> buffer_ = nil;
    size_t size_ = 0;
};

}
