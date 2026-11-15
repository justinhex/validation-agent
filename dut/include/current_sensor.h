#pragma once

class WindowMotor;

class CurrentSensor{
public:
    explicit CurrentSensor(const WindowMotor& motor);
    int getCurrent() const; //mA
private:
    const WindowMotor& motor_;
};