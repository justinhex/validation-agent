#include "door_handle.h"

void DoorHandle::pull() {
    pulled_ = true;
}

void DoorHandle::release() {
    pulled_ = false;
}

bool DoorHandle::isPulled() const {
    return pulled_;
}