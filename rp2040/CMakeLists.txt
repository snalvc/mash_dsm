cmake_minimum_required(VERSION 3.16)

if(NOT DEFINED PICO_SDK_PATH)
  message(FATAL_ERROR "you must define PICO_SDK_PATH")
endif()

include(${PICO_SDK_PATH}/pico_sdk_init.cmake)

set(PROJ_NAME mash_dsm)

project(${PROJ_NAME} C CXX ASM)

pico_sdk_init()

add_executable(${PROJ_NAME} main.c mash_dsm.s)

# Link with the pico stdlib
target_link_libraries(${PROJ_NAME} pico_stdlib pico_multicore)

# Create map/bin/hex/uf2 files
pico_add_extra_outputs(${PROJ_NAME})