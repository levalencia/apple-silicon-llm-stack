#include <Metal/Metal.h>
#include <memory>

namespace metal_inference {

class MetalDevice {
public:
    MetalDevice() {
        device_ = MTLCreateSystemDefaultDevice();
    }
    
    ~MetalDevice() = default;
    
    MetalDevice(const MetalDevice&) = delete;
    MetalDevice& operator=(const MetalDevice&) = delete;
    
    MetalDevice(MetalDevice&&) noexcept = default;
    MetalDevice& operator=(MetalDevice&&) noexcept = default;
    
    auto is_available() const -> bool { return device_ != nullptr; }
    auto handle() const -> id<MTLDevice> { return device_; }
    auto queue() const -> id<MTLCommandQueue> { return queue_; }
    
private:
    id<MTLDevice> device_ = nullptr;
    id<MTLCommandQueue> queue_ = nullptr;
};

}
