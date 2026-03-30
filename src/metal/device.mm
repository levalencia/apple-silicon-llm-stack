#include <Metal/Metal.h>
#include <memory>

namespace metal_inference {

// IMPORTANT (Objective-C++ / ARC):
// We use Objective-C++ (.mm) to seamlessly mix C++ with Apple's Metal framework.
// Even though we aren't using Automatic Reference Counting (ARC) explicitly here,
// interacting with id<MTLDevice> and id<MTLCommandQueue> requires Objective-C
// object semantics, which Objective-C++ handles natively without bridging overhead.
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
