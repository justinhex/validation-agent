# Power Window - Requirements 
**This model was developed to test validation-agent.**

- **PW-001**: One-touch close shall fully close the window within 4 seconds of the switch being pressed up.
- **PW-002**: If an obstruction is detected while closing, the window shall reverse direction within 100 ms and open at least 50 mm.
- **PW-003**: The window shall ignore switch inputs for 500 ms after an anti-pinch reversal, to avoid immediate re-triggering.
- **PW-004**: The window position shall be reported on the CAN bus every 100 ms with an accuracy of plus or minus 2 mm.
- **PW-005**: If the window motor current exceeds 900 mA for more than 200 ms while closing, the controller shall treat it as an obstruction.
- **PW-006**: When a door handle is pulled, the window shall drop 10 mm to clear the door seal; when the door is closed, the window shall raise back to fully closed.
- **PW-007**: After a power loss or ignition cycle, the window shall re-learn its fully-closed position on the first close operation.
- **PW-008**: On a vent command, the window shall open to a vent position 25 mm from fully closed.