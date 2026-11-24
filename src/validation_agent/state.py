from typing import TypedDict


class AgentState(TypedDict):
    pack_root_ : str
    reqirements_ : list[dict]
    plan_ : dict | None
    generated_files_ : list[str]
    review_ : dict | None
    human_decision_ : str | None
    manifest_ : dict | None
    extra_context_ : dict | None
    current_step_ : str