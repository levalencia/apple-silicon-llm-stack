#include <metal_stdlib>
using namespace metal;

kernel void matmul(
    device const half* A [[buffer(0)]],
    device const half* B [[buffer(1)]],
    device float* C [[buffer(2)]],
    uint2 gid [[thread_position_in_grid]],
    uint2 tgid [[threadgroup_position_in_grid]],
    uint2 tid [[thread_position_in_threadgroup]],
    uint sgid [[simdgroup_index_in_threadgroup]]
) {
    simdgroup_float8x8 acc;
    simdgroup_half8x8 a_tile, b_tile;
    
    simdgroup_matrix_fill(acc, 0.0f);
    
    const uint K = 8;  // Tile size
    
    for (uint k = 0; k < K; k += 8) {
        simdgroup_load(a_tile, A + (gid.y * K + k) * 8, 8);
        simdgroup_load(b_tile, B + (k * 8) + gid.x * 8, 8);
        simdgroup_multiply_accumulate(acc, a_tile, b_tile, acc);
    }
    
    simdgroup_store(acc, C + (gid.y * 8) + gid.x * 8, 8);
}
