cmake_minimum_required(VERSION 3.28)
project(metal-inference-core VERSION 0.1.0 LANGUAGES CXX OBJCXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

option(ENABLE_SANITIZERS "Enable sanitizers (ASan/TSan/UBSan)" OFF)
option(ENABLE_TESTING "Enable testing" ON)
option(ENABLE_METAL_TESTS "Enable Metal-specific tests" ON)

if(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
    set(BIN_DIR "bin")
    set(LIB_DIR "lib")
else()
    set(BIN_DIR "bin/${CMAKE_CURRENT_SOURCE_DIR}")
    set(LIB_DIR "lib/${CMAKE_CURRENT_SOURCE_DIR}")
endif()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

include(CompilerWarnings)
include(Sanitizers)

# Fetch dependencies
include(FetchContent)

FetchContent_Declare(spdlog
    GIT_REPOSITORY https://github.com/gabime/spdlog.git
    GIT_TAG v1.15.0
    FIND_PACKAGE_ARGS
)
FetchContent_MakeAvailable(spdlog)

add_subdirectory(src)

if(ENABLE_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()

if(CMAKE_BUILD_TYPE MATCHES Debug)
    add_subdirectory(benchmarks)
endif()
