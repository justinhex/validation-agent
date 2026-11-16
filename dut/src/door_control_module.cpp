#include "door_control_module.h"
#include "can_bus.h"
#include "current_sensor.h"
#include "door_handle.h"
#include "hall_sensor.h"
#include "window_motor.h"


DoorControlModule::DoorControlModule(
    WindowMotor& window_motor,
    HallSensor& hall_sensor,
    DoorHandle& door_handle,
    CurrentSensor& current_sensor,
    CanBus& can_bus,
    WindowSwitch& window_switch
) : ECU("DoorControlModule"),
    window_motor_(window_motor),
    hall_sensor_(hall_sensor),
    door_handle_(door_handle),
    current_sensor_(current_sensor),
    can_bus_(can_bus),
    window_switch_(window_switch)
{
}

void DoorControlModule::tick(int ms) {
    if(ignore_timer_ms_ > 0){
        ignore_timer_ms_ -= ms;
    }
    if(last_window_switch_state_ != window_switch_.getState() && ignore_timer_ms_ <= 0){
        if(window_switch_.getState() == WindowSwitch::State::kUp){
            
            if(window_motor_.getDirection() == WindowMotor::kDirectionClose){
                window_motor_.setDirection(WindowMotor::kDirectionStop);
            }else{
                window_motor_.setDirection(WindowMotor::kDirectionClose);
            }
        } else if(window_switch_.getState() == WindowSwitch::State::kDown){
            
            if(window_motor_.getDirection() == WindowMotor::kDirectionOpen){
                window_motor_.setDirection(WindowMotor::kDirectionStop);
            }else{
                window_motor_.setDirection(WindowMotor::kDirectionOpen);
            }
        }

        if(window_switch_.getState() != WindowSwitch::State::kReleased && moving_to_target_){
            moving_to_target_ = false;
        }
    }

    // Handle door handle pull/release events
    if(last_handle_pulled_ != door_handle_.isPulled()){
        if(door_handle_.isPulled() && hall_sensor_.getPosition() <= WindowMotor::kFullyClosedMm){
            target_position_mm_ = kDoorOpenDropMm;
            moving_to_target_ = true;
        }else if(!door_handle_.isPulled()){
            target_position_mm_ = WindowMotor::kFullyClosedMm;
            moving_to_target_ = true;
        }
        last_handle_pulled_ = door_handle_.isPulled();
    }
    
    // Handle anti-pinch logic
    if(window_motor_.getDirection() == WindowMotor::kDirectionClose &&
        current_sensor_.getCurrent() >= kPinchCurrentMa){
                pinch_timer_ms_ += ms;            
    }else{
        pinch_timer_ms_ = 0;
    }

    if(pinch_timer_ms_ >= kPinchConfirmMs){
        window_motor_.setDirection(WindowMotor::kDirectionOpen);
        pinch_reversing_ = true;
        ignore_timer_ms_ = kIgnorePinchMs;
        pinch_timer_ms_ = 0;
        target_position_mm_ = hall_sensor_.getPosition() + kPinchRevertMm > WindowMotor::kFullyOpenMm ?
         WindowMotor::kFullyOpenMm : hall_sensor_.getPosition() + kPinchRevertMm;
        moving_to_target_ = true;
    }
    if(moving_to_target_){
        if(target_position_mm_ > hall_sensor_.getPosition()){
            window_motor_.setDirection(WindowMotor::kDirectionOpen);
        }else if (target_position_mm_ < hall_sensor_.getPosition()){
            window_motor_.setDirection(WindowMotor::kDirectionClose);
        }else{
            window_motor_.setDirection(WindowMotor::kDirectionStop);
            moving_to_target_ = false;
            if(pinch_reversing_){
                pinch_reversing_ = false;
                ignore_timer_ms_ = kIgnorePinchMs;
            }
        }
    }

    // Window motor tick
    window_motor_.tick(ms);
    if(hall_sensor_.getPosition() <= WindowMotor::kFullyClosedMm ||
        hall_sensor_.getPosition() >= WindowMotor::kFullyOpenMm){
        
        if(hall_sensor_.getPosition()<= WindowMotor::kFullyClosedMm){
            calibrated_ = true;
        }
        window_motor_.setDirection(WindowMotor::kDirectionStop);
    }
    last_window_switch_state_ = window_switch_.getState();

    // Send CAN message every 100ms
    can_timer_ms_ += ms;
    if(can_timer_ms_ >= kCanSendMs){
        can_bus_.sendPosition(hall_sensor_.getPosition());
        can_timer_ms_ = 0;
    }
}

void DoorControlModule::requestVent() {
    moving_to_target_ = true;
    target_position_mm_ = kVentPositionMm; // Use the defined constant for vent position
}

void DoorControlModule::powerOff() {
    ECU::powerOff();
    calibrated_ = false;
    pinch_timer_ms_ = 0;
    ignore_timer_ms_ = 0;
    target_position_mm_ = 0;
    can_timer_ms_ = 0;
    moving_to_target_ = false;
    pinch_reversing_ = false;
    last_handle_pulled_ = door_handle_.isPulled();
    last_window_switch_state_ = window_switch_.getState();
    window_motor_.setDirection(WindowMotor::kDirectionStop);
}