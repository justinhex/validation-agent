#include "window_api.h"
#include "body_control_module.h"
#include "door_control_module.h"
#include "can_bus.h"
#include "current_sensor.h"
#include "door_handle.h"
#include "hall_sensor.h"
#include "window_motor.h"
#include "window_switch.h"


struct WindowApi
{
    CanBus can_bus_;
    WindowMotor winodw_motor_;
    WindowSwitch window_switch_;
    HallSensor hall_sensor_;
    CurrentSensor current_sensor_;
    DoorHandle door_handle_;
    DoorControlModule dcm_;
    BodyControlModule bcm_;

    WindowApi() 
        :   bcm_(can_bus_, dcm_),
            dcm_(winodw_motor_, 
                hall_sensor_, 
                door_handle_,
                current_sensor_,
                can_bus_,
                window_switch_
            ),
            hall_sensor_(winodw_motor_),
            current_sensor_(winodw_motor_)          
    {
    }
};


extern "C"{

    WindowApi* window_create(void){
        return new WindowApi();
    }

    void window_destroy(WindowApi* api){
        delete api;
    }

    void window_press_up(WindowApi* api){
        api->window_switch_.pressUp();
    }

    void window_press_down(WindowApi* api){
        api->window_switch_.pressDown();
    }

    void window_release(WindowApi* api){
        api->window_switch_.release();
    }

    void window_tick(WindowApi* api, int ms){
        api->dcm_.tick(ms);
        api->bcm_.tick(ms);
    }

    void window_pull_door_handle(WindowApi* api){
        api->door_handle_.pull();
    }

    void window_close_door(WindowApi* api){
        api->door_handle_.release();
    }
    
    void window_vent(WindowApi* api){
        api->dcm_.requestVent();
    }

    void window_power_cycle(WindowApi* api){
        api->dcm_.powerOff();
        api->bcm_.powerOff();
        api->dcm_.powerOn();
        api->bcm_.powerOn();
    }

    int window_position_mm(WindowApi* api){
        return api->hall_sensor_.getPosition();
    }

    int window_current_ma(WindowApi* api){
        return api->current_sensor_.getCurrent();
    }

    int window_can_position_mm(WindowApi* api){
        return api->bcm_.getWindowPosition();
    }
}