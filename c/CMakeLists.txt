cmake_minimum_required(VERSION 3.16)
project(stack_vm C)

set(CMAKE_C_STANDARD 99)

add_executable(stack_vm main.c re.h parser.h)
target_link_libraries(stack_vm -lpcre.dll -lpcreposix.dll)

add_custom_target(CopyBin
        COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/bin/ ${CMAKE_CURRENT_BINARY_DIR}
        )

add_dependencies(stack_vm CopyBin)