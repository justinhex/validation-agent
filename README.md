# Validation Agent

An AI agent that does a test engineer's job — requirements in, tested product out. The goal is to test everything, including HIL on real hardware, pure software, apps, and games — any product that needs validation.

> Work in progress. The requirements parser, LLM client, CI, and the demo DUT core (ECU + DoorControlModule) are done; test generation, test automation, the bench API, and log triage are on the roadmap below.

## The problem

Validation is slow because a test engineer does the same mechanical work on every program: read the requirement, write the test, write the glue code, run the bench, read the log, find the fault. HIL benches are one place this work happens — the work itself is the same everywhere, and it is all automatable.

The goal of this project is to automate the test engineer's entire job with AI: requirements in, tested product out, no human in the loop for the mechanical parts.

## What this will do

1. **Requirements → BDD tests** — feed in a requirements document, get permanent pytest-bdd feature files. An LLM writes the test cases like a test developer: one scenario per behavior, Given-When-Then, every scenario tagged with its requirement ID.
2. **BDD → test automation scripts** — the feature files are turned into executable test scripts (pytest-bdd step definitions driving the bench) automatically, so the tests run without hand-writing glue code.
3. **Log triage** — feed in a test log, get a ranked list of anomalies with a suspected root cause and a suggested next check.

The agent's capabilities are packaged as agent skills in `skills/` — one skill per capability.

## Status

- [x] Requirements parser — reads a requirements doc into Requirement objects (`src/hil_validation/requirements_parser.py`)
- [x] Demo requirements — power-window requirements (`examples/requirements_power_window.md`)
- [x] LLM client — OpenAI-compatible API, any LLM via base URL / model / key (fake mode for testing without a key)
- [x] CI (GitHub Actions) — builds the C++ DUT and compile-checks the Python code on every PR and push to main; `build-dut` and `check-python` are required status checks
- [x] Demo DUT core — simulated window controller in C++ (ECU, DoorControlModule, WindowMotor, HallSensor, CurrentSensor, WindowSwitch, DoorHandle, CanBus; anti-pinch implemented in the DCM)
- [ ] Test generator — LLM writes pytest-bdd `.feature` files from requirements
- [ ] Test automation scripts — generate executable pytest-bdd step definitions from the `.feature` files
- [ ] Bench API — the bench that drives the DUT (SIL now, real hardware/HIL later — same test cases, only the backend swaps)
- [ ] BodyControlModule — listens to the DCM's CAN position broadcasts, forwards vent commands
- [ ] Log triage
- [ ] Jenkins monitor
- [ ] Bazel build

## Try the parser

```bash
python src/hil_validation/requirements_parser.py
```

Prints the 8 power-window requirements with their IDs and source file.

## Build the DUT

```bash
cmake -S dut -B dut/build -G "Visual Studio 18 2026" -A x64
cmake --build dut/build --config Release
```

On Windows, double-click `dut_build.bat` for the same build.

Builds `window_dut.dll`, the simulated window system (ECU, DoorControlModule, motor, Hall and current sensors, switch, door handle, CAN bus). Requires Visual Studio 2026 with the Desktop development with C++ workload and CMake 4.2+.

The DUT is a shared library: the same test cases drive the simulated DUT (SIL) now and real hardware on a bench (HIL) later — only the bench backend changes.

## Project layout

```text
README.md
.github/
  pull_request_template.md       # PR description template
  workflows/ci.yml               # GitHub Actions: build the DUT + check Python syntax
dut/
  CMakeLists.txt                 # builds window_dut (shared library)
  include/                       # ecu.h, door_control_module.h
  src/                           # ecu.cpp, door_control_module.cpp
  simulate/
    include/                     # window_motor.h, hall_sensor.h, current_sensor.h, window_switch.h, door_handle.h, can_bus.h
    src/                         # window_motor.cpp, hall_sensor.cpp, current_sensor.cpp, window_switch.cpp, door_handle.cpp, can_bus.cpp
  build/                         # (ignored) CMake output, window_dut.dll
dut_build.bat                    # double-click build (Windows)
examples/
  requirements_power_window.md   # power-window requirements
skills/
  generate-tests/SKILL.md        # agent skill: LLM writes BDD test cases from requirements
  generate-scripts/SKILL.md      # (coming) agent skill: generate test automation scripts from .feature files
src/hil_validation/
  __init__.py
  requirements_parser.py         # parse a requirements doc into Requirement objects
  llm_client.py                  # OpenAI-compatible LLM client
tests/                           # (coming) pytest-bdd feature files + step definitions
```

## Tech stack

Python 3.10+ for the parser and LLM client; C++17, CMake, and Visual Studio 2026 for the demo DUT. pytest and pytest-bdd are planned for the test suite. The LLM layer speaks the OpenAI-compatible API, so the same code runs with OpenAI, DeepSeek, a local model, or any OpenAI-compatible endpoint — just change the base URL, model, and key.

## Contributing

Direct pushes to `main` are blocked — all changes go through a pull request:

1. Create a branch from `main` (`git checkout -b <branch-name>`).
2. Make your change. Commit with an area prefix, for example `DUT: ...`, `Test: ...`, `CI: ...`, `Docs: ...`.
3. Push the branch and open a pull request. Fill in the PR template (PR Content / Added / Design notes / Verification / What's next).
4. CI must be green before merge: `build-dut` (C++ DUT build) and `check-python` (Python syntax check) are required status checks on `main`.

Check locally before pushing:

```bash
cmake -S dut -B dut/build -G "Visual Studio 18 2026" -A x64
cmake --build dut/build --config Release
python -m compileall src
```

## License

MIT. Sample data is fictional.
