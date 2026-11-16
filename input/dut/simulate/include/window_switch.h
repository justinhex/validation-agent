#pragma once

class WindowSwitch{
public:
    enum class State{
        kUp,
        kDown,
        kReleased
    };
    void pressUp();
    void pressDown();
    void release();
    State getState() const;

private:
    State state_ = State::kReleased;
};