#include "current_sensor.h"
#include "window_motor.h"

CurrentSensor::CurrentSensor(const WindowMotor& motor) : motor_(motor){

}

int CurrentSensor::getCurrent() const{
    
    return motor_.getCurrent();

}