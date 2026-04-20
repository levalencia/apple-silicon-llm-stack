add_library(project_warnings INTERFACE)

target_compile_options(project_warnings INTERFACE
    -Wall -Wextra -Wpedantic
    -Werror
    -Wno-unused-parameter
    -Wshadow -Wnon-virtual-dtor -Woverloaded-virtual
)

if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    target_compile_options(project_warnings INTERFACE
        -Wconversion -Wsign-conversion
    )
endif()
