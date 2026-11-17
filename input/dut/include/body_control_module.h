#pragma once
#include "ecu.h"

class CanBus;
class DoorControlModule;

class BodyControlModule : public ECU {
public:
    BodyControlModule(
        CanBus& can_bus,
        DoorControlModule& door_control_module
    );
    
    void tick(int ms) override;
    void powerOff() override;
    void requestVent();
    int getWindowPosition() const;

private:
    CanBus& can_bus_;
    DoorControlModule& dcm_;
    int last_window_position_mm_ = 0;

};