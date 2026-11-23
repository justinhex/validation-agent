# Purpose: Verify LLMClient.generate() calls the OpenAI-compatible API
#          correctly and that fake mode bypasses the API.
# Scenarios:
#   - generate returns the mocked API response content.
#   - generate passes the correct model and prompt to the API.
#   - fake mode returns a fixed string without calling the API.

import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

from validation_agent.llm_client import LLMClient

@patch("validation_agent.llm_client.OpenAI")
def test_llm_generate_returns_content(mock_openai):
    mock_client = mock_openai.return_value
    mock_reponse = MagicMock()
    mock_reponse.choices[0].message.content = "Fake response content..."
    mock_client.chat.completions.create.return_value = mock_reponse

    llm_client = LLMClient(
        base_url= os.getenv("HIL_BASE_URL"),
        model= os.getenv("HIL_MODEL"),
        api_key= os.getenv("HIL_API_KEY")
    )

    result = llm_client.generate("Test Generate Function...")

    assert result == "Fake response content..."
    mock_client.chat.completions.create.assert_called_once_with(
        os.getenv("HIL_MODEL"),
        messages=[{
            "role": "user",
            "content": "Test Generate Function..."
        }],
        temperature=0,
        max_tokens=8192,
        extra_body={
            "options":{"num_ctx": 8192}
        }
    )


def test_llm_generate_fake_model():
    llm_client = LLMClient(
        base_url= "fake",
        model="fake",
        api_key="fake"
    )

    result = llm_client.generate("Test Generate Function with Fake Model...")

    assert result == "Fake response for prompt: "\
        "Test Generate Function with Fake Model..."