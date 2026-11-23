import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMClient:

    def __init__(self, base_url: str, model: str, api_key: str="ollama"):

        self.base_url_ = base_url
        self.model_ = model
        self.api_key_ = api_key
        self.llm_client_ = OpenAI(
            api_key = self.api_key_,
            base_url = self.base_url_
        )

    

    def generate(self, prompt: str) -> str:
        """
        Generate a response from the LLM based on the given prompt.

        Args:
            prompt (str): The input prompt for the LLM.

        Returns:
            str: The generated response from the LLM.
        """
        if self.model_ == "fake":
            return f"Fake response for prompt: {prompt}" #Help bypass LLM by set HIL_MODEL = fake
                                                        #and only test validation agent frameware
        else:
            #Extra Configuration For LLM
            options = {
                "num_ctx" : 8192,
            }

            response = self.llm_client_.chat.completions.create(
                self.model_,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=8192, #Max size of single output message
                extra_body={"options":options}
            )
            return response.choices[0].message.content


if __name__ == "__main__":

    llm_client = LLMClient(os.getenv("HIL_BASE_URL"), os.getenv("HIL_MODEL"), os.getenv("HIL_API_KEY"))

    print(llm_client.generate("Hello, how are you?"))