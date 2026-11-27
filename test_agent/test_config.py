import sys
import pytest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)
from validation_agent.config import Settings
from validation_agent.config import load_settings
from validation_agent.config import model_config

@pytest.fixture
def build_env_path(tmp_path):
    env_path = tmp_path / ".env.fake"
    env_path.write_text(
        "PLANNER_BASE_URL='https://planner:9999/v1'\n"\
        "PLANNER_MODEL='planner-model:128B'\n"\
        "PLANNER_API_KEY='planner-api-key'\n"\
        "HIL_BASE_URL='https://hil:8888/v1'\n"\
        "HIL_MODEL='hil-model:128B'\n"\
        "HIL_API_KEY='hil-api-key'\n"\
        "LLM_TEMPERATURE=0.2\n"\
        "LLM_MAX_TOKENS=1024\n"\
        "LLM_NUM_CTX=1024\n"\
        "LLM_TIMEOUT_S=100\n"\
        "MAX_REVIEW_ATTEMPTS=3\n"\
        "MCP_CALL_BUDGET=20\n"\
        "PYTEST_TIMEOUT_S=600\n"\
        "CHECKPOINT_PATH=.checkpoints/checkpoints.sqlite\n",
        encoding = "utf-8"        
    )
    return env_path


def test_load_settings_normal(build_env_path):

    settings = load_settings(env_path=build_env_path)

    assert isinstance(settings, Settings)
    assert len(settings.models) == 2
    planner_config = model_config(settings, "planner")
    hil_config = model_config(settings, "hil")
    assert planner_config.base_url == "https://planner:9999/v1"
    assert planner_config.model == "planner-model:128B"
    assert planner_config.api_key == "planner-api-key"
    assert hil_config.base_url == "https://hil:8888/v1"
    assert hil_config.model == "hil-model:128B"
    assert hil_config.api_key == "hil-api-key"
    assert planner_config.temperature == 0.2
    assert hil_config.temperature == 0.2
    assert planner_config.max_tokens == 1024
    assert hil_config.max_tokens == 1024
    assert planner_config.num_ctx == 1024
    assert hil_config.num_ctx == 1024
    assert planner_config.timeout == 100
    assert hil_config.timeout == 100

def test_load_settings_dynamic(build_env_path):
    with build_env_path.open("a", encoding="utf-8") as f:
        f.write(
            "REVIEWER_BASE_URL='https://reviewer:9999/v1'\n"\
            "REVIEWER_MODEL='reviewer-model:128B'\n"\
            "REVIEWER_API_KEY='reviewer-api-key'\n"
        )

    settings = load_settings(env_path=build_env_path)

    assert isinstance(settings, Settings)
    assert len(settings.models) == 3
    reviewer_config = model_config(settings, "reviewer")
    assert reviewer_config.base_url == "https://reviewer:9999/v1"
    assert reviewer_config.model == "reviewer-model:128B"
    assert reviewer_config.api_key == "reviewer-api-key"
    assert reviewer_config.temperature == 0.2
    assert reviewer_config.max_tokens == 1024
    assert reviewer_config.num_ctx == 1024
    assert reviewer_config.timeout == 100


def test_missing_model(tmp_path):
    env_path = tmp_path / ".env.fake"
    env_path.write_text(
        "REVIEWER_BASE_URL='https://reviewer:9999/v1'\n"\
        "LLM_TEMPERATURE=0.2\n"\
        "LLM_MAX_TOKENS=1024\n"\
        "LLM_NUM_CTX=1024\n"\
        "LLM_TIMEOUT_S=100\n"\
        "MAX_REVIEW_ATTEMPTS=3\n"\
        "MCP_CALL_BUDGET=20\n"\
        "PYTEST_TIMEOUT_S=600\n"\
        "CHECKPOINT_PATH=.checkpoints/checkpoints.sqlite\n",
        encoding = "utf-8"
    )

    with pytest.raises(ValueError):
        load_settings(env_path=env_path)


def test_no_role(tmp_path):
    env_path = tmp_path / ".env.fake"
    env_path.write_text(
        "LLM_TEMPERATURE=0.2\n"\
        "LLM_MAX_TOKENS=1024\n"\
        "LLM_NUM_CTX=1024\n"\
        "LLM_TIMEOUT_S=100\n"\
        "MAX_REVIEW_ATTEMPTS=3\n"\
        "MCP_CALL_BUDGET=20\n"\
        "PYTEST_TIMEOUT_S=600\n"\
        "CHECKPOINT_PATH=.checkpoints/checkpoints.sqlite\n",
        encoding = "utf-8"
    )

    with pytest.raises(ValueError):
        load_settings(env_path=env_path)


def test_missing_param(tmp_path):
    
    env_path = tmp_path / ".env.fake"
    env_path.write_text(
        "REVIEWER_BASE_URL='https://reviewer:9999/v1'\n"\
        "REVIEWER_MODEL='reviewer-model:128B'\n"\
        "REVIEWER_API_KEY='reviewer-api-key'\n"
        "LLM_MAX_TOKENS=1024\n"\
        "LLM_NUM_CTX=1024\n"\
        "LLM_TIMEOUT_S=100\n"\
        "MAX_REVIEW_ATTEMPTS=3\n"\
        "MCP_CALL_BUDGET=20\n"\
        "PYTEST_TIMEOUT_S=600\n"\
        "CHECKPOINT_PATH=.checkpoints/checkpoints.sqlite\n",
        encoding = "utf-8"
    )

    with pytest.raises(ValueError):
        load_settings(env_path=env_path)


def test_role_missing(tmp_path):
    
    env_path = tmp_path / ".env.fake"
    env_path.write_text(
        "REVIEWER_BASE_URL='https://reviewer:9999/v1'\n"\
        "REVIEWER_MODEL='reviewer-model:128B'\n"\
        "REVIEWER_API_KEY='reviewer-api-key'\n"
        "LLM_TEMPERATURE=0.2\n"\
        "LLM_MAX_TOKENS=1024\n"\
        "LLM_NUM_CTX=1024\n"\
        "LLM_TIMEOUT_S=100\n"\
        "MAX_REVIEW_ATTEMPTS=3\n"\
        "MCP_CALL_BUDGET=20\n"\
        "PYTEST_TIMEOUT_S=600\n"\
        "CHECKPOINT_PATH=.checkpoints/checkpoints.sqlite\n",
        encoding = "utf-8"
    )

    settings = load_settings(env_path=env_path)

    assert settings.langsmith_api_key == None

    with pytest.raises(KeyError):
        model_config(settings, "planner")