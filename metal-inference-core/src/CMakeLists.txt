add_library(inference_core STATIC
    core/engine.cpp
    core/model_loader.cpp
    core/sampler.cpp
)

target_include_directories(inference_core PUBLIC
    ${CMAKE_SOURCE_DIR}/include
)

target_link_libraries(inference_core
    PUBLIC spdlog::spdlog
)

target_compile_features(inference_core PUBLIC cxx_std_20)

if(ENABLE_SANITIZERS)
    enable_sanitizer(address)
endif()

add_library(inference_metal STATIC
    metal/device.mm
    metal/compute_pipeline.mm
    metal/buffer_pool.mm
)

target_include_directories(inference_metal PRIVATE
    ${CMAKE_SOURCE_DIR}/include
)

target_link_libraries(inference_metal
    PRIVATE inference_core
    PRIVATE "-framework Metal"
    PRIVATE "-framework Foundation"
    PRIVATE "-framework MetalPerformanceShaders"
)

add_executable(inference_cli
    ../tools/main.cpp
)

target_include_directories(inference_cli PRIVATE
    ${CMAKE_SOURCE_DIR}/include
)

target_link_libraries(inference_cli
    PRIVATE inference_core
    PRIVATE inference_metal
)
