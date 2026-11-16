#pragma once

class DoorHandle{
public:
    void pull();
    void release();
    bool isPulled() const;
private:
    bool pulled_ = false;
};