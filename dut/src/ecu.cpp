#include "ecu.h"


ECU::ECU(std::string name) : name_(name){

}

void ECU::init(){
    powered_ = false;
}

void ECU::tick(int ms){

}

void ECU::powerOn(){

    powered_ = true;

}

void ECU::powerOff(){
    powered_ = false;
}

bool ECU::isPowered() const{
    return powered_;
}

const std::string& ECU::getName() const{
    return name_;
}