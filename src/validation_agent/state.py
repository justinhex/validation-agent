from typing import TypedDict


class AgentState(TypedDict):
    pack_root: str
    requirements: list[dict]
    plan: dict | None
    generated_files: list[str]
    review: dict | None
    human_decision: str | None
    manifest: dict | None
    extra_context: dict | None
    current_step: str