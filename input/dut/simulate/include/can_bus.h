#pragma once

class CanBus{
public:
    void sendPosition(int position_mm);
    int getLastPosition() const;
private:
    int last_position_ = 0;
};