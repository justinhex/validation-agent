#include "window_motor.h"

WindowMotor::WindowMotor(){

}

void WindowMotor::setDirection(int direction){
    
    direction_ = direction;
    if(direction_ = kDirectionStop){
        stalled_ = false;
    }

}

int WindowMotor::getDirection() const{
    return direction_;
}

void WindowMotor::tick(int ms){

    if(blocked_ == true){
        stalled_ = true;
        return;
    }

    position_ += direction_ * ms * kSpeedmmPerSec / 1000;
    if(position_ <= kFullyClosedMm){
        position_ = kFullyClosedMm;
        stalled_ = (direction_ == kDirectionClose);
    } else if(position_ >= kFullyOpenMm){
        position_ = kFullyOpenMm;
        stalled_ = (direction_ == kDirectionOpen);
    }else{
        stalled_ = false;
    }
}

int WindowMotor::getPosition() const{
    
    return position_;

}

int WindowMotor::getCurrent() const{

    if(direction_ == kDirectionStop){
        return 0;
    }
    
    return stalled_ ? kStallCurrent : kNormalCurrent;
}

void WindowMotor::setBlocked(bool blocked){
    
    blocked_ = blocked;
    if(!blocked_){
        stalled_ = false;
    }

}