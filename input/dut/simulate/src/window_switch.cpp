#include "window_switch.h"


void WindowSwitch::pressUp() {
    state_ = State::kUp;
}

void WindowSwitch::pressDown() {
    state_ = State::kDown;
}

void WindowSwitch::release() {
    state_ = State::kReleased;
}

WindowSwitch::State WindowSwitch::getState() const {
    return state_;
}
