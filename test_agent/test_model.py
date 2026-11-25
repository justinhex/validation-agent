import sys
from pathlib import Path
from langchain_openai import ChatOpenAI
from unittest.mock import patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

from validation_agent.model import create_chat_model


def test_create_chat_model_return():
    base_url = "testing_url"
    model = "testing_model"
    api_key = "testing_key"

    chat_client = create_chat_model(
        base_url=base_url,
        model=model,
        api_key=api_key
    )

    assert isinstance(chat_client, ChatOpenAI)

@patch("validation_agent.model.ChatOpenAI")
def test_param_passed_correctly(mock_chatopenai):
    chat_client = create_chat_model(
        base_url="testing_url",
        model="testing_model",
        api_key="testing_key"
    )

    mock_chatopenai.assert_called_once_with(
        base_url="testing_url",
        model="testing_model",
        api_key="testing_key",  
        temperature=0.0,
        max_tokens=8192,
        timeout=120,
        extra_body={
            "options":{"num_ctx":8192}
        }
    )

    assert chat_client is mock_chatopenai.return_value

@patch("validation_agent.model.ChatOpenAI")
def test_param_passed_modify(mock_chatopenai):
    chat_client = create_chat_model(
        base_url="testing_url",
        model="testing_model",
        api_key="testing_key",
        temperature=2.0,
        max_tokens=1024,
        num_ctx=1024,
        timeout=30
    )

    mock_chatopenai.assert_called_once_with(
        base_url="testing_url",
        model="testing_model",
        api_key="testing_key",
        temperature=2.0,
        max_tokens=1024,
        timeout=30,       
        extra_body={
            "options":{"num_ctx":1024}
        }
    )

    assert chat_client is mock_chatopenai.return_value
   