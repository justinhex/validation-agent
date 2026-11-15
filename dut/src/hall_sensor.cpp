#include "hall_sensor.h"
#include "window_motor.h"

HallSensor::HallSensor(const WindowMotor& motor) : motor_(motor){

}

int HallSensor::getPosition() const{
    
    return motor_.getPosition();

}


