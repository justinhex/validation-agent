cmake_minimum_required(VERSION 3.15)
project(validation-agent-dut)

set(CMAKE_CXX_STANDARD 17)

add_library(window_dut SHARED
    src/ecu.cpp
    src/door_control_module.cpp
    src/body_control_module.cpp
    simulate/src/window_motor.cpp
    simulate/src/hall_sensor.cpp
    simulate/src/current_sensor.cpp
    simulate/src/window_switch.cpp
    simulate/src/door_handle.cpp
    simulate/src/can_bus.cpp
    src/window_api.cpp
)

target_include_directories(window_dut PUBLIC
    include
    simulate/include
)