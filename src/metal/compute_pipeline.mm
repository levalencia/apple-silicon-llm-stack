#include <Metal/Metal.h>
#include <MetalKit/MetalKit.h>
#include <memory>
#include <vector>

namespace metal_inference {

class ComputePipeline {
public:
    ComputePipeline(id<MTLDevice> device, id<MTLFunction> function) {
        NSError* error = nil;
        pipeline_ = [device newComputePipelineStateWithFunction:function error:&error];
    }
    
    auto handle() const -> id<MTLComputePipelineState> { return pipeline_; }
    
private:
    id<MTLComputePipelineState> pipeline_ = nil;
};

class MetalBufferPool {
public:
    explicit MetalBufferPool(id<MTLDevice> device) : device_(device) {}
    
    auto allocate(size_t size) -> id<MTLBuffer> {
        return [device_ newBufferWithLength:size 
                options:MTLResourceStorageModeShared];
    }
    
    void release(id<MTLBuffer> buffer) {
        // Metal automatically manages memory
    }
    
private:
    id<MTLDevice> device_;
};

}
