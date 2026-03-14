add_executable(unit_tests 
    unit/main.cpp
)

target_include_directories(unit_tests PRIVATE
    ${CMAKE_SOURCE_DIR}/include
)

target_link_libraries(unit_tests PRIVATE
    inference_core
    inference_metal
)

enable_testing()
add_test(NAME UnitTests COMMAND unit_tests)
