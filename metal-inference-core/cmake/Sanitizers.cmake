macro(enable_sanitizer SANITIZER_TYPE)
    if(NOT ENABLE_SANITIZERS)
        return()
    endif()
    
    set(SANITIZER_FLAGS "")
    
    if(${SANITIZER_TYPE} STREQUAL "address")
        set(SANITIZER_FLAGS "-fsanitize=address -fno-omit-frame-pointer")
    elseif(${SANITIZER_TYPE} STREQUAL "thread")
        set(SANITIZER_FLAGS "-fsanitize=thread")
    elseif(${SANITIZER_TYPE} STREQUAL "undefined")
        set(SANITIZER_FLAGS "-fsanitize=undefined")
    endif()
    
    add_compile_options(${SANITIZER_FLAGS})
    add_link_options(${SANITIZER_FLAGS})
endmacro()
