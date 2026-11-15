# Validation Agent

AI-assisted test generation, test automation, and log triage for HIL validation — any hardware, not just automotive.

> Work in progress. The requirements parser, LLM client, and CI are done, and the demo DUT core is merged; test generation, test automation, the rest of the demo DUT, and log triage are on the roadmap below.

## The problem

Writing validation tests from requirements is slow, and triaging HIL failure logs by hand is slower. Validation engineers repeat the same mechanical work on every program: read the requirement, write the test, write the glue code, run the bench, read the log, find the fault.

## What this will do

1. **Requirements → BDD tests** — feed in a requirements document, get permanent pytest-bdd feature files. An LLM writes the test cases like a test developer: one scenario per behavior, Given-When-Then, every scenario tagged with its requirement ID.
2. **BDD → test automation scripts** — the feature files are turned into executable test scripts (pytest-bdd step definitions driving the bench) automatically, so the tests run without hand-writing glue code.
3. **Log triage** — feed in a HIL log, get a ranked list of anomalies with a suspected root cause and a suggested next check.

The agent's capabilities are packaged as agent skills in `skills/` — one skill per capability.

## Status

- [x] Requirements parser — reads a requirements doc into Requirement objects (`src/hil_validation/requirements_parser.py`)
- [x] Demo requirements — power-window requirements (`examples/requirements_power_window.md`)
- [x] LLM client — OpenAI-compatible API, any LLM via base URL / model / key (fake mode for testing without a key)
- [x] CI (GitHub Actions) — builds the C++ DUT and compile-checks the Python code on every PR and push to main; `build-dut` and `check-python` are required status checks
- [ ] Test generator — LLM writes pytest-bdd `.feature` files from requirements
- [ ] Test automation scripts — generate executable pytest-bdd step definitions from the `.feature` files
- [ ] Demo DUT — simulated window controller in C++ (core merged: ECU, WindowMotor, HallSensor, CurrentSensor; DoorControlModule, BodyControlModule, CanBus, and the bench API are next; anti-pinch is the first exercise)
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

Builds `window_dut.dll`, the simulated window system (ECU, motor, Hall and current sensors). Requires Visual Studio 2026 with the Desktop development with C++ workload and CMake 4.2+.

## Project layout

```text
README.md
.github/
  pull_request_template.md       # PR description template
  workflows/ci.yml               # GitHub Actions: build the DUT + check Python syntax
dut/
  CMakeLists.txt                 # builds window_dut (shared library)
  include/                       # ecu.h, window_motor.h, hall_sensor.h, current_sensor.h, ...
  src/                           # ecu.cpp, window_motor.cpp, hall_sensor.cpp, current_sensor.cpp, ...
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

## License

MIT. Sample data is fictional.
