from langchain_openai import ChatOpenAI

def create_chat_model(
        base_url: str,
        model: str,
        api_key: str,
        *,
        temperature: float = 0,
        max_tokens: int = 8192,
        num_ctx: int = 8192,
        timeout: int = 120,
) -> ChatOpenAI:
    openai_client = ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        extra_body={
            "options": {"num_ctx": num_ctx}
        }
    )

    return openai_client