# Validation Agent

An AI agent that does a test engineer's job — requirements in, tested product out. The focus is HIL validation on real hardware, starting with embedded systems. The ultimate vision is to test everything — pure software, apps, games, any product that needs validation.

> Work in progress. The requirements parser, input loader, model layer (LangChain ChatOpenAI), config layer, multi-agent state, CI, and the demo DUT core (ECU, DoorControlModule, BodyControlModule, window_api) are done; the LangGraph multi-agent graph, test generation, the Python bench, and log triage are on the roadmap below.

## The problem

Validation is slow because a test engineer does the same mechanical work on every program: read the requirement, write the test, write the glue code, run the bench, read the log, find the fault. On a HIL bench, that work is slow, expensive, and repetitive — and it is all automatable.

The goal of this project is to automate the test engineer's entire job with AI, starting with HIL validation: requirements in, tested product out, no human in the loop for the mechanical parts.

## What this will do

1. **Requirements → BDD tests** — feed in a requirements document, get permanent pytest-bdd feature files. An LLM writes the test cases like a test developer: one scenario per behavior, Given-When-Then, every scenario tagged with its requirement ID.
2. **BDD → test automation scripts** — the feature files are turned into executable test scripts (pytest-bdd step definitions driving the bench) automatically, so the tests run without hand-writing glue code.
3. **Run the tests** — run the generated pytest suite on the bench (simulated DUT now, real hardware later) and get a pass/fail report with logs.
4. **Log triage** — feed in a test log, get a ranked list of anomalies with a suspected root cause and a suggested next check.

The agent's capabilities are packaged as agent skills in `skills/` — one skill per capability.

## Status

- [x] Requirements parser — reads a requirements doc into Requirement objects (`src/validation_agent/helpers/requirements_parser.py`)
- [x] Input loader — loads the files a planner lists into memory (`src/validation_agent/helpers/input_loader.py`): parses the planner JSON, validates each path stays inside the pack root and exists, returns `{relative_path: file_contents}`; `ValueError` on malformed JSON, escaping paths, or empty/missing `files`; `FileNotFoundError` only when a file is genuinely missing inside the pack
- [x] Demo requirements — power-window requirements (`input/requirements/requirements_power_window.md`)
- [x] Model layer — LangChain ChatOpenAI factory (`src/validation_agent/model.py`): `create_chat_model` builds a configured ChatOpenAI per agent (base URL, model, key, temperature, max_tokens, num_ctx, timeout); points at the local Ollama endpoint or any OpenAI-compatible API
- [x] Config layer — loads settings from `.env` (`src/validation_agent/config.py`): `Settings` holds a `models` dict keyed by lowercase role name, so each LLM role gets its own endpoint (`<ROLE>_BASE_URL` / `<ROLE>_MODEL` / `<ROLE>_API_KEY`); roles are discovered by scanning for `*_BASE_URL`, so adding a role is three lines in `.env` with no code change; shared parameters (temperature, max_tokens, num_ctx, timeout) are read once and shared by all roles; missing required values raise `ValueError`; reads are isolated per call (`dotenv_values`), so tests never pollute each other
- [x] Multi-agent state — shared graph state (`src/validation_agent/state.py`): `AgentState` (TypedDict) with pack_root, requirements, plan, generated_files, review, review_attempts, human_decision, manifest, extra_context, current_step
- [x] Prompt engineer — builds the prompt for each task from the pack, compresses it, checks it against the context window, and picks which LLM runs it (`src/validation_agent/prompt_engineering.py`)
- [x] Platform tests — pytest suite for the agent itself (`test_agent/`): input-loader + model + PromptEngineering + requirements_parser + config, 24 tests passing; runs in CI via the `test-agent` job
- [x] CI (GitHub Actions) — builds the C++ DUT, compile-checks the Python code, and runs the platform tests (`test_agent/`) on every PR and push to main; `build-dut`, `check-python`, and `test-agent` are required status checks
- [x] Demo DUT core — simulated window controller in C++ (ECU, DoorControlModule, BodyControlModule, WindowMotor, HallSensor, CurrentSensor, WindowSwitch, DoorHandle, CanBus; anti-pinch implemented in the DCM; `window_api` C layer exposes the DUT to the Python bench)
- [ ] Multi-agent graph — LangGraph StateGraph (Supervisor → Planner → Generator → Reviewer) + driver; LangChain + LangGraph used as one stack
- [ ] Test generator — LLM writes pytest-bdd `.feature` files from requirements
- [ ] Test automation scripts — generate executable pytest-bdd step definitions from the `.feature` files
- [x] Bench API (C layer) — `window_api` exposes the DUT to the bench (`window_create` / `window_destroy` + press, release, tick, position, current, vent, power cycle)
- [ ] Python bench — drives the DUT through the C API via `ctypes` (SIL now, real hardware/HIL later — same test cases, only the backend swaps); generated by the LLM via the `generate-bench` skill, never hand-written
- [ ] Test execution — run the generated pytest suite on the bench and collect results and logs
- [x] BodyControlModule — listens to the DCM's CAN position broadcasts, forwards vent commands
- [ ] Log triage
- [ ] Jenkins monitor
- [ ] Bazel build

## Usage

### Run the platform tests

```bash
pip install -r requirements.txt
pytest test_agent/ -v
```

24 tests: input-loader (8) + model (3) + PromptEngineering (4) + requirements_parser (3) + config (6). The same suite runs in CI via the `test-agent` job.

### Parse a requirements document

```python
from validation_agent.helpers.requirements_parser import parse_requirements

reqs = parse_requirements("input/requirements/requirements_power_window.md")
for req in reqs:
    print(f"{req.req_id}: {req.description} (from {req.path})")
```

The parser reads `- **PW-001**: ...` bullets from a markdown file and returns a list of `Requirement` objects (`req_id`, `description`, `path`), in document order.

The LLM layer (model + prompt engineer) is in place and configured via `.env` — see Tech stack below. Test generation, the Python bench, and log triage are on the roadmap and not yet usable.

## Build the DUT

```bash
cmake -S input/dut -B input/dut/build -G "Visual Studio 18 2026" -A x64
cmake --build input/dut/build --config Release
```

On Windows, double-click `input/dut/dut_build.bat` for the same build.

Builds `window_dut.dll`, the simulated window system (ECU, DoorControlModule, BodyControlModule, motor, Hall and current sensors, switch, door handle, CAN bus, plus the `window_api` C layer for the Python bench). Requires Visual Studio 2026 with the Desktop development with C++ workload and CMake 4.2+.

The DUT is a shared library: the same test cases drive the simulated DUT (SIL) now and real hardware on a bench (HIL) later — only the bench backend changes.

## Project layout

```text
README.md
.github/
  pull_request_template.md       # PR description template
  workflows/ci.yml               # GitHub Actions: build the DUT + check Python syntax + run platform tests
input/
  main_instruction.md            # pack entry point: the planner LLM reads it to understand the task, decide which skills and files are needed, and summarize them into a prompt; also holds overview, output rules, pointers to instructions
  pack.yaml                      # pack manifest: name, version, path overrides
  requirements/
    requirements_power_window.md # power-window requirements
  dut/
    CMakeLists.txt               # builds window_dut (shared library)
    include/                     # ecu.h, door_control_module.h, body_control_module.h, window_api.h
    src/                         # ecu.cpp, door_control_module.cpp, body_control_module.cpp, window_api.cpp
    simulate/
      include/                   # window_motor.h, hall_sensor.h, current_sensor.h, window_switch.h, door_handle.h, can_bus.h
      src/                       # window_motor.cpp, hall_sensor.cpp, current_sensor.cpp, window_switch.cpp, door_handle.cpp, can_bus.cpp
    build/                       # (ignored) CMake output, window_dut.dll
    dut_build.bat                # double-click build (Windows)
  context/                       # user environment background (CI design, environment, version control)
  instruction/                   # project-specific steps (flash, failure handling, tools, JIRA)
skills/
  generate-tests/SKILL.md        # agent skill: LLM writes BDD test cases from requirements
  generate-bench/SKILL.md        # agent skill: LLM writes the Python bench (bench.py) from the DUT header + requirements
  generate-scripts/SKILL.md      # (coming) agent skill: generate test automation scripts from .feature files
src/validation_agent/
  __init__.py
  helpers/
    __init__.py
    requirements_parser.py       # parse a requirements doc into Requirement objects
    input_loader.py              # load the files a planner lists into memory (load_inputs)
  model.py                       # ChatOpenAI factory: create_chat_model builds a configured ChatOpenAI per agent (base URL, model, key, temperature, max_tokens, num_ctx, timeout)
  config.py                      # load settings from .env: Settings + AgentModelConfig, per-role LLM endpoints discovered from *_BASE_URL
  prompt_engineering.py          # build, compress, and size-check prompts; pick the LLM per task (PromptEngineering class)
  state.py                       # AgentState (TypedDict): shared multi-agent state (pack_root, requirements, plan, generated_files, review, review_attempts, human_decision, manifest, extra_context, current_step)
test_agent/                      # platform tests (pytest): input-loader + model + PromptEngineering + requirements_parser + config, 24 tests
tests/                           # (coming) pytest-bdd feature files + step definitions
```

## Tech stack

Python 3.10+ for the parser and model layer; C++17, CMake, and Visual Studio 2026 for the demo DUT. pytest is in use for the platform test suite (`test_agent/`, pinned in `requirements.txt`); pytest-bdd is planned for the generated test suite. The LLM layer is LangChain's ChatOpenAI (`langchain-openai`), and the multi-agent orchestration is LangGraph (`langgraph`) — one stack, pinned in `requirements.txt`. Each LLM role has its own base URL, model, and key in `.env`, loaded by `config.py` into a per-role `AgentModelConfig` (never hardcoded), so the same code runs with a third-party LLM (OpenAI, DeepSeek), a local model (Ollama), or an LLM fine-tuned and trained on this platform for validation work — and each role can point at a different LLM. The base URL points to a validation-specialized LLM; fine-tuning and training that model is a future goal of the project.

## Contributing

Direct pushes to `main` are blocked — all changes go through a pull request:

1. Create a branch from `main` (`git checkout -b <branch-name>`).
2. Make your change. Commit with an area prefix, for example `DUT: ...`, `Test: ...`, `CI: ...`, `Docs: ...`.
3. Push the branch and open a pull request. Fill in the PR template (PR Content / Added / Design notes / Verification / What's next).
4. CI must be green before merge: `build-dut` (C++ DUT build), `check-python` (Python syntax check), and `test-agent` (platform tests) are required status checks on `main`.

5. At least one member's review and approval is required before merge.

Check locally before pushing:

```bash
cmake -S input/dut -B input/dut/build -G "Visual Studio 18 2026" -A x64
cmake --build input/dut/build --config Release
python -m compileall src
```

## License

MIT. Sample data is fictional.
