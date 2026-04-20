#include <metal_stdlib>
using namespace metal;

/**
 * @brief High-performance Matrix Multiplication Shader for Apple Silicon (M-series)
 *
 * This compute shader performs matrix multiplication (C = A * B) optimized for the 
 * Apple M4 Pro architecture. It leverages SIMD-group (single instruction, multiple data) 
 * matrix instructions to perform math in parallel directly on the GPU ALUs.
 * 
 * Hardware context: Apple Silicon has Unified Memory (UMA), meaning the GPU reads 
 * from the exact same physical RAM as the CPU. The `device` address space here points 
 * directly to that shared RAM without needing a PCIe bus transfer.
 */
kernel void matmul(
    // `device` indicates these buffers are in global GPU memory (Unified Memory)
    // `half` is used for 16-bit float (FP16), saving 50% memory bandwidth over 32-bit floats.
    device const half* A [[buffer(0)]],
    device const half* B [[buffer(1)]],
    device float* C [[buffer(2)]],
    
    // Position of this specific thread within the entire grid of work
    uint2 gid [[thread_position_in_grid]],
    
    // Position of the threadgroup (a block of threads executing together)
    uint2 tgid [[threadgroup_position_in_grid]],
    
    // Position of the thread within its specific threadgroup
    uint2 tid [[thread_position_in_threadgroup]],
    
    // The specific SIMD group (warp) this thread belongs to
    uint sgid [[simdgroup_index_in_threadgroup]]
) {
    // simdgroup_matrix types map directly to Apple Silicon AMX (Apple Matrix Coprocessor)
    // or GPU tensor cores, allowing an entire 8x8 matrix operation in one clock cycle.
    simdgroup_float8x8 acc;
    simdgroup_half8x8 a_tile, b_tile;
    
    // Initialize the accumulator matrix with zeros
    simdgroup_matrix_fill(acc, 0.0f);
    
    // We process the matrices in tiles of 8x8 to maximize L1 cache hits 
    // and fit perfectly into the SIMD registers.
    const uint K = 8;  // Tile size
    
    for (uint k = 0; k < K; k += 8) {
        // Load an 8x8 tile from Matrix A and Matrix B into fast SIMD registers
        // Apple Silicon unified memory enables very fast coalesced reads here.
        simdgroup_load(a_tile, A + (gid.y * K + k) * 8, 8);
        simdgroup_load(b_tile, B + (k * 8) + gid.x * 8, 8);
        
        // Fused Multiply-Accumulate (MAC): acc = (a_tile * b_tile) + acc
        // This is the workhorse of LLM inference (computing attention and feed-forward layers)
        simdgroup_multiply_accumulate(acc, a_tile, b_tile, acc);
    }
    
    // Store the 8x8 result tile back into global memory (Matrix C)
    simdgroup_store(acc, C + (gid.y * 8) + gid.x * 8, 8);
}
