cmake_minimum_required(VERSION 3.15)
project(validation-agent-dut)

set(CMAKE_CXX_STANDARD 17)

add_library(window_dut SHARED
    src/ecu.cpp
    src/window_motor.cpp
    src/hall_sensor.cpp
    src/current_sensor.cpp    
)

target_include_directories(window_dut PUBLIC include)