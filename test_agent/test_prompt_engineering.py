import sys
import pytest

from pathlib import Path
from unittest.mock import patch

# Make src/ importable so the test can import validation_agent.
# Test lives in test_agent/, two levels below the repo root.
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent/"src")
)

from validation_agent.prompt_engineering import PromptEngineering

# Purpose: test PromptEngineering.prepare() in
# src/validation_agent/prompt_engineering.py — the prompt build /
# size-check / LLM-select logic. Fake inputs only, no real files,
# no LLM call.
#
# Scenarios:
#   1. test_bench_prompt — normal path: bench_prompt fits in 8192
#      tokens, prepare returns the bench prompt and selects the
#      validation LLM.
#   2. test_prompt_oversize_real_check — oversize path, real check:
#      max_tokens=1 forces check_size to fail, prepare switches to
#      compress_prompt and returns the planner LLM.
#   3. test_prompt_overize_mock_check_fail — oversize path, mocked
#      check: force check_size to fail, verify prepare's branching
#      in isolation (independent of the real len//4 estimate).
#   4. test_prompt_oversize_mock_check_pass — normal path, mocked
#      check: force check_size to pass, verify prepare keeps the
#      bench_prompt task and selects the validation LLM.

'''
-----------------------------------------------------------------------
'''

# Fake inputs for bench_prompt. TASK_PARTS["bench_prompt"] needs the
# header, requirements and skill keys — only the keys matter, the
# values are arbitrary strings.
@pytest.fixture
def fake_inputs():

    return {
        "header": "fake header content",
        "requirements": "fake requirement content",
        "skill": "fake skill content",
    }


# Normal path: prompt fits in 8192 tokens, prepare returns the bench
# prompt as-is and selects the validation LLM.
def test_bench_prompt(fake_inputs):
    pe = PromptEngineering("bench_prompt")
    prompt, llm = pe.prepare(fake_inputs, 8192)
    assert llm == "validation"
    assert prompt.count("## ") == 3 # 3 keys for bench_prompt

# Oversize path, real check: max_tokens=1 forces check_size to fail,
# prepare switches to compress_prompt and returns the planner LLM.
def test_prompt_oversize_real_check(fake_inputs):
    pe = PromptEngineering("bench_prompt")
    prompt, llm = pe.prepare(fake_inputs, 1)
    assert llm == "planner"
    assert prompt.count("## ") == 5   # count("## ") is 5, not 2 — the embedded original prompt itself
    assert pe.current_task_ == "compress_prompt"    # contains 3 "## " markers.

# Oversize path, mocked check: force check_size to fail so prepare's
# branching is tested in isolation, independent of the real len//4
# size estimate.
def test_prompt_overize_mock_check_fail(fake_inputs):
    pe = PromptEngineering("bench_prompt")
    with patch.object(pe, "check_size", return_value=False) as mock_check:
        prompt, llm = pe.prepare(fake_inputs, 8192)
    assert llm == "planner"
    assert prompt.count("## ") == 5   # count("## ") is 5, not 2 — the embedded original prompt itself
    assert pe.current_task_ == "compress_prompt"    # contains 3 "## " markers.
    mock_check.assert_called_once()

# Normal path, mocked check: force check_size to pass, verify prepare
# keeps the bench_prompt task and selects the validation LLM.
def test_prompt_oversize_mock_check_pass(fake_inputs):
    pe = PromptEngineering("bench_prompt")
    with patch.object(pe, "check_size", return_value=True) as mock_check:
        prompt, llm = pe.prepare(fake_inputs, 8192)
        assert llm == "validation"
        assert prompt.count("## ") == 3
        assert pe.current_task_ == "bench_prompt"
        mock_check.assert_called_once()



