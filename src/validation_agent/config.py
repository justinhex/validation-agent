from dotenv import dotenv_values
from pathlib import Path
from dataclasses import dataclass



@dataclass(frozen=True)
class AgentModelConfig:
    base_url: str
    model: str
    api_key: str
    temperature: float = 0.0
    max_tokens: int = 8192
    num_ctx: int = 8192
    timeout: int = 120

    def to_kwargs(self) -> dict:
        return {
            "base_url": self.base_url,
            "model": self.model,
            "api_key": self.api_key,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "num_ctx": self.num_ctx,
            "timeout": self.timeout,
        }

@dataclass(frozen=True)
class Settings:
    models: dict[str, AgentModelConfig]
    temperature: float
    max_tokens: int
    num_ctx: int
    llm_timeout_s: int
    max_review_attempts: int
    mcp_call_budget: int
    pytest_timeout_s: int
    checkpoint_path: Path
    langsmith_api_key: str | None

def _required(values: dict, name: str) -> str:
    value = values.get(name)
    if value is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return value

def load_settings(env_path: Path | None = None) -> Settings:

    values = dotenv_values(env_path)
    temperature = float(_required(values, "LLM_TEMPERATURE"))
    max_tokens = int(_required(values, "LLM_MAX_TOKENS"))
    num_ctx = int(_required(values, "LLM_NUM_CTX"))
    llm_timeout_s = int(_required(values, "LLM_TIMEOUT_S"))
    max_review_attempts = int(_required(values, "MAX_REVIEW_ATTEMPTS"))
    mcp_call_budget = int(_required(values, "MCP_CALL_BUDGET"))
    pytest_timeout_s = int(_required(values, "PYTEST_TIMEOUT_S"))
    checkpoint_path = Path(_required(values, "CHECKPOINT_PATH"))
    langsmith_api_key = values.get("LANGSMITH_API_KEY")

    models = _load_model_configs(
        values,
        temperature=temperature,
        max_tokens=max_tokens,
        num_ctx=num_ctx,
        timeout=llm_timeout_s,
    )

    return Settings(
        models=models,
        temperature=temperature,
        max_tokens=max_tokens,
        num_ctx=num_ctx,
        llm_timeout_s=llm_timeout_s,
        max_review_attempts=max_review_attempts,
        mcp_call_budget=mcp_call_budget,
        pytest_timeout_s=pytest_timeout_s,
        checkpoint_path=checkpoint_path,
        langsmith_api_key=langsmith_api_key
    )

def _load_model_configs(values: dict, *, temperature: float, max_tokens: int, num_ctx: int, timeout: int) -> dict[str, AgentModelConfig]:
    models: dict[str, AgentModelConfig] = {}
    for name in values:
        if not name.endswith("_BASE_URL"):
            continue
        prefix = name[: -len("_BASE_URL")]
        role = prefix.lower()
        models[role] = AgentModelConfig(
            base_url=_required(values, f"{prefix}_BASE_URL"),
            model=_required(values, f"{prefix}_MODEL"),
            api_key=_required(values, f"{prefix}_API_KEY"),
            temperature=temperature,
            max_tokens=max_tokens,
            num_ctx=num_ctx,
            timeout=timeout,
        )
    if not models:
        raise ValueError("No LLM roles found in .env (expected at least one *_BASE_URL variable)")
    return models

def model_config(s: Settings, role: str):
    try:
        return s.models[role]
    except KeyError:
        raise KeyError
                

    