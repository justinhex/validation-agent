#pragma once
#include <string>

class ECU {
public:
    explicit ECU(std::string name);
    virtual ~ECU() = default;

    virtual void init(); //initial ecu power state
    virtual void tick(int ms); //execute by tick, update status
    virtual void powerOff();

    void powerOn();
    bool isPowered() const;
    const std::string& getName() const;

protected:
    std::string name_;
    bool powered_ = false;
};