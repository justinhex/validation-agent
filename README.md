# Validation Agent

AI-assisted test generation and log triage for HIL validation — any hardware, not just automotive.

> Work in progress. The requirements parser is done; LLM test generation, the demo DUT, and CI are on the roadmap below.

## The problem

Writing validation tests from requirements is slow, and triaging HIL failure logs by hand is slower. Validation engineers repeat the same mechanical work on every program: read the requirement, write the test, run the bench, read the log, find the fault.

## What this will do

1. **Requirements → BDD tests** — feed in a requirements document, get permanent pytest-bdd feature files. An LLM writes the test cases like a test developer: one scenario per behavior, Given-When-Then, every scenario tagged with its requirement ID.
2. **Log triage** — feed in a HIL log, get a ranked list of anomalies with a suspected root cause and a suggested next check.

The agent's capabilities are packaged as agent skills in `skills/` — one skill per capability.

## Status

- [x] Requirements parser — reads a requirements doc into Requirement objects (`src/hil_validation/requirements_parser.py`)
- [x] Demo requirements — power-window requirements (`examples/requirements_power_window.md`)
- [x] LLM client — OpenAI-compatible API, any LLM via base URL / model / key (fake mode for testing without a key)
- [ ] Test generator — LLM writes pytest-bdd `.feature` files from requirements
- [ ] Demo DUT — simulated window controller in C++ (anti-pinch is the first exercise)
- [ ] Step definitions — pytest-bdd steps driving the bench
- [ ] Log triage
- [ ] Jenkins monitor + CI (GitHub Actions, Jenkinsfile, Bazel)

## Try the parser

```bash
python src/hil_validation/requirements_parser.py
```

Prints the 8 power-window requirements with their IDs and source file.

## Project layout

```text
README.md
examples/
  requirements_power_window.md   # power-window requirements
skills/
  generate-tests/SKILL.md        # agent skill: LLM writes BDD test cases from requirements
src/hil_validation/
  __init__.py
  requirements_parser.py         # parse a requirements doc into Requirement objects
  llm_client.py                  # OpenAI-compatible LLM client (coming)
tests/                           # (coming) pytest-bdd feature files + step definitions
```

## Tech stack

Python 3.10+, pytest, pytest-bdd. The LLM layer speaks the OpenAI-compatible API, so the same code runs with OpenAI, DeepSeek, a local model, or any OpenAI-compatible endpoint — just change the base URL, model, and key.

## License

MIT. Sample data is fictional.
