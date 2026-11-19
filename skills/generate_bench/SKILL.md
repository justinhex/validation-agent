# generate-bench

## Purpose

Generate a Python bench (`bench.py`) that drives a DUT through its C API via `ctypes`. The bench is the only path tests use to touch the DUT.

The bench is generated fresh for each DUT. It is never hand-written and never edited by hand. If the generated bench is wrong, fix the input (the DUT header or the requirements) or fix this skill, then regenerate.

## When to use

When a DUT (new, or with a changed C API) needs a Python bench so tests can drive it. Input is the DUT's C API header and the requirements; output is `bench.py`.

## Inputs

- **DUT C API header** (e.g. `input/dut/include/window_api.h`) — the contract. Read it to learn every function's name, parameters, and return type. Do not invent a function that is not in the header, and do not omit one that is.
- **Requirements** (e.g. `input/requirements/requirements_power_window.md`) — context on what the bench must support. Example: PW-004 needs both a true position and a CAN position, so the bench must expose both; PW-007 needs power-cycle to clear calibration, so the bench must power-cycle the whole system.
- **DLL path** — the built DUT library (e.g. `input/dut/build/Release/window_dut.dll`).

## Output

A single `bench.py` file.

## Rules

1. Load the DLL with `ctypes.CDLL`. Use the path given by the caller; do not hardcode a machine-specific absolute path unless told to.
2. Declare every C function's `argtypes` and `restype` explicitly. Never let `ctypes` guess. A missing or wrong declaration corrupts pointers and crashes.
3. Map C types to `ctypes` types:
   - pointer (e.g. `WindowApi*`) → `ctypes.c_void_p`
   - `int` → `ctypes.c_int`
   - `void` return → `restype = None`
   - no parameters → `argtypes = []`
4. Wrap the C API in a Python class (e.g. `Bench`) whose methods match the Bench API. Each method calls the matching C function through the handle.
5. Handle lifetime: create the handle on init, destroy it on close — including on failure. Provide a `close()` method and support `with` (context manager) so the handle is always released.
6. Expose every function the header declares. No more, no less.
7. When the DUT has two position sources, expose both: the true position (e.g. Hall sensor) and the CAN-cached position (e.g. BCM cache), so tests can compare them (PW-004).
8. Current comes from the current sensor directly, never over CAN. CAN carries position only.
9. Power cycle is a whole-system off-off-on-on: power off every ECU, then power on every ECU. After it, calibration is cleared, so the next close re-learns (PW-007).
10. Include a `main` / smoke block: create the bench, drive it (e.g. press up/down, tick), and print the positions so a human can see the DUT actually move. This is the acceptance check.

## Example (power window)

Header `window_api.h` declares `window_create` / `window_destroy` plus 11 functions: `press_up` / `press_down` / `release`, `tick`, `position_mm`, `current_ma`, `pull_door_handle` / `close_door`, `vent`, `power_cycle`, `can_position_mm`. The generated `bench.py` wraps all 11, exposes `position_mm` (Hall sensor, true position) and `can_position_mm` (BCM CAN cache) separately, and its smoke block closes then opens the window and prints the position moving.

## Verification

Run the generated `bench.py` smoke block against the built DLL. The position must actually change. If it does not move, or the process crashes, the bench is wrong. Do not hand-edit `bench.py`. Fix the input or this skill, then regenerate.
