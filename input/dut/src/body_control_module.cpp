#include "body_control_module.h"
#include "can_bus.h"
#include "door_control_module.h"


BodyControlModule::BodyControlModule(
    CanBus& can_bus,
    DoorControlModule& door_control_module
) : ECU("BodyControlModule"), can_bus_(can_bus), dcm_(door_control_module)
{
}

void BodyControlModule::tick(int ms) {
   last_window_position_mm_ = can_bus_.getLastPosition();
}

void BodyControlModule::powerOff(){
    ECU::powerOff();
    last_window_position_mm_ = 0;
}

void BodyControlModule::requestVent() {
    dcm_.requestVent();
}

int BodyControlModule::getWindowPosition() const {
    return last_window_position_mm_;
}