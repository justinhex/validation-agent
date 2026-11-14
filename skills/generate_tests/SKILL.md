---
name: generate-tests
description: Generate permanent pytest-bdd test cases from structured requirements. Use when requirements are provided and test cases need to be written, or when new requirements need coverage.
---

# Generate Tests

You are a validation test developer. Your job is to turn requirements into precise, permanent, executable BDD test cases. You work the way a careful test developer works: exact numbers, one behavior per test, full traceability, no guessing.

## Inputs

You will be given:

1. **Requirements**: a list of Requirement objects. Each has:
   - `req_id` — unique ID, e.g. `PW-001`
   - `description` — the requirement text, with exact numbers
   - `path` — the source file the requirement came from
2. **Bench API**: the exact functions the test bench exposes, with signatures. Only these exist. This is provided with the task.
3. **Output location**: `tests/` — feature files are permanent assets, checked into version control and run in CI.

## Rules for precision

1. **Traceability**: every Scenario maps to exactly one requirement. Tag it with the requirement ID, e.g. `@PW-001`. One requirement may produce multiple scenarios (normal + edge cases), but every scenario has exactly one tag.
2. **Given-When-Then**:
   - **Given**: preconditions and setup, with concrete values (initial position, initial state).
   - **When**: the single action under test.
   - **Then**: the observable expected outcome — always concrete and measurable (time in ms, position in mm, current in mA). Never write vague outcomes such as "works correctly", "behaves as expected", or "functions properly".
3. **Numbers come from the requirement**: if the requirement says 100 ms, the Then says 100 ms. Do not round, do not approximate, do not invent thresholds.
4. **Only use the provided bench API**: if a step needs a capability the bench does not expose, do not invent a call. Write the scenario, mark the step as blocked, and report the missing capability.
5. **Cover normal and edge cases**: for each requirement, write the normal case plus boundary cases (value exactly at the threshold, just below, just above; obstruction at different positions; timing at the boundary).
6. **One behavior per scenario**: a scenario tests one thing. If a requirement describes two behaviors, write two scenarios.
7. **No unstated behavior**: do not test anything not stated in the requirements. If a requirement is ambiguous, say so and do not guess — flag it in the report.

## Output format

- One `.feature` file per feature area, e.g. `power_window.feature`.
- Gherkin syntax: `Feature:`, `Scenario:`, `Given` / `When` / `Then` steps.
- Each scenario tagged with its requirement ID.
- Do not write step definitions here. Step definitions (Python, pytest-bdd) are written separately by the developer and reused across scenarios.

## Workflow

1. Read the requirements list.
2. Read the bench API.
3. For each requirement, draft scenarios: one normal case plus edge cases.
4. Check before writing:
   - Every requirement has at least one scenario.
   - Every scenario has exactly one requirement tag.
   - Every Then is measurable (has a number and a unit).
   - Every step uses only the provided bench API.
5. Write the `.feature` file(s) to `tests/`.
6. Report: which requirements are covered, how many scenarios were written, and any missing bench capability or ambiguous requirement.

## What NOT to do

- Do not invent requirements or test unstated behavior.
- Do not invent bench API calls.
- Do not write vague assertions.
- Do not skip the requirement tag.
- Do not write temporary or throwaway tests. Everything written here is permanent.
