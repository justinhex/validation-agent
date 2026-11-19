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
    model = os.getenv("HIL_MODEL")
    if model == "fake":
        return f"Fake response for prompt: {prompt}" #Help bypass LLM by set HIL_MODEL = fake
                                                     #and only test validation agent frameware
    else:
        #Extra Configuration For LLM
        options = {
            "num_ctx" : 8192,
        }

        #Init LLM
        client = OpenAI(
            api_key=os.getenv("HIL_API_KEY"), 
            base_url=os.getenv("HIL_BASE_URL")
        )

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=8192, #Max size of single output message
            extra_body={"options":options}
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    
    print(generate("Hello, how are you?"))