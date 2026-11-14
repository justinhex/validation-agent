import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def generate(prompt: str) -> str:
    """
    Generate a response from the LLM based on the given prompt.

    Args:
        prompt (str): The input prompt for the LLM.

    Returns:
        str: The generated response from the LLM.
    """
    model = os.getenv("HIL_MODEL", "gpt-4o-mini")
    if model == "fake":
        return f"Fake response for prompt: {prompt}"
    else:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"), 
            base_url=os.getenv("OPENAI_BAESE_URL", "https://api.openai.com/v1")
        )

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=4096,
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    
    print(generate("Hello, how are you?"))