#pragma once

class WindowMotor;

class HallSensor{ //read motor, getting window position
public:
    explicit HallSensor(const WindowMotor& motor);
    int getPosition() const; // mm
private:
    const WindowMotor& motor_;
};