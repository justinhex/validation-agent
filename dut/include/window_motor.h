#pragma once

class WindowMotor{
public:
    static constexpr int kFullyClosedMm = 0;
    static constexpr int kFullyOpenMm  = 400;
    static constexpr int kDirectionStop = 0;
    static constexpr int kDirectionOpen = 1;
    static constexpr int kDirectionClose = -1;
    static constexpr int kNormalCurrent = 150;
    static constexpr int kStallCurrent = 1200;
    static constexpr int kSpeedmmPerSec = 100;//  mm/s

    WindowMotor();
    void setDirection(int direction); // +1 opening, -1 closing, 0 stop
    void tick(int ms);
    int getPosition() const; //mm, 0 = fully closed, 400 - fully opened
    int getCurrent() const; //mA, 0 stop, 150 normal, 1200 stall
    void setBlocked(bool blocked);
private:
    int position_ = 0;
    int direction_ = 0;
    bool stalled_ = false;
    bool blocked_ = false;
};