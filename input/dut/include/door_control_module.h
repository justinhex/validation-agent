#pragma once
#include "ecu.h"
#include "window_switch.h"


class CanBus;
class CurrentSensor;
class DoorHandle;
class HallSensor;
class WindowMotor;

class DoorControlModule : public ECU {
public:
    DoorControlModule(
        WindowMotor& window_motor,
        HallSensor& hall_sensor,
        DoorHandle& door_handle,
        CurrentSensor& current_sensor,
        CanBus& can_bus,
        WindowSwitch& window_switch
    );

    void tick(int ms) override;
    void powerOff() override;

    void requestVent();
private:
    static constexpr int kVentPositionMm = 25;
    static constexpr int kPinchRevertMm = 50;
    static constexpr int kDoorOpenDropMm = 10;

    static constexpr int kPinchCurrentMa = 900;
    static constexpr int kPinchConfirmMs = 200;
    static constexpr int kIgnorePinchMs = 500;
    static constexpr int kCanSendMs = 100;


    WindowMotor& window_motor_;
    HallSensor& hall_sensor_;
    DoorHandle& door_handle_;
    CurrentSensor& current_sensor_;
    CanBus& can_bus_;
    WindowSwitch& window_switch_;

    int pinch_timer_ms_ = 0; // avoid mistriggering pinch detection, triggered after 200ms
    int ignore_timer_ms_ = 0; // avoid re-pinch when window switch is still held down
    int target_position_mm_ = 0;
    int can_timer_ms_ = 0; // send can message every 100ms
    bool moving_to_target_ = false;
    bool calibrated_ = true;
    bool pinch_reversing_ = false;
    bool last_handle_pulled_ = false;
    WindowSwitch::State last_window_switch_state_ = WindowSwitch::State::kReleased;
};