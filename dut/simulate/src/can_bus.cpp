#include "can_bus.h"

void CanBus::sendPosition(int position_mm) {
    last_position_ = position_mm;
}

int CanBus::getLastPosition() const {
    return last_position_;
}
