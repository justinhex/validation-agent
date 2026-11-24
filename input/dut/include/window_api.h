#pragma once


#ifdef __cplusplus
extern "C" {
#endif

typedef struct WindowApi WindowApi;
WindowApi* window_create(void);
void window_destory(WindowApi* api);

void window_press_up(WindowApi* api);
void window_press_down(WindowApi* api);
void window_release(WindowApi* api);
void window_tick(WindowApi* api, int ms);
void window_pull_door_handle(WindowApi* api);
void window_close_door(WindowApi* api);
void window_vent(WindowApi* api);
void window_power_cycle(WindowApi* api);


int window_position_mm(WindowApi* api);
int window_current_ma(WindowApi* api);
int window_can_position_mm(WindowApi* api);



#ifdef __cplusplus
}
#endif