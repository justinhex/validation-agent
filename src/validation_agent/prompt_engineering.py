# Task types for current_task:
#   1. plan_prompt: planner decides what skills + requirements + context
#      information are needed to finish other tasks. Does not generate
#      test cases itself. Uses planner LLM.
#      e.g. main_instruction.md path + read-main-instruction skill + planner LLM.
#   2. testcase_prompt: requirement + skill + validation LLM.
#      Generates feature files (BDD test cases) from requirements.
#   3. bench_prompt: DUT header (e.g. window_api.h) + requirements
#      + generate-bench skill + validation LLM. Generates bench.py.
#   4. pipeline_prompt: context + skill + validation LLM.
#      Generates CI / Jenkinsfile.
#   5. automate_prompt: BDD test cases (feature) + skill + validation LLM.
#      Generates step definitions (pytest automation).
#   6. triage_prompt: test case results + skills + validation LLM.
#      May involve RAG, MCP. Triages failures.
#   7. compress_prompt: long prompt + skill + planner LLM.
#      Summarizes the prompt into a shorter, reasonable version
#      that keeps what the skill needs. Uses planner LLM.
import os

TASK_PARTS = {   
    "plan_prompt": ["main_instruction", "skill"],
    "testcase_prompt": ["requirements", "skill"],
    "bench_prompt": ["header", "requirements", "skill"],
    "pipeline_prompt": ["context", "skill"],
    "automate_prompt": ["feature", "skill"],
    "triage_prompt": ["results", "skill"],
    "compress_prompt": ["prompt", "skill"],
}

class PromptEngineering:


    def __init__(self, current_task):
        self.current_task_ = current_task 


    def build_prompt(self, inputs):
        #Assemble the prompt for the current task from its inputs.
        #inputs:
        #e.g {"skill": /content/of/skills, "requirements": /what/user/wants/to/run, "...": /info/that/task/need/to/finish e.g header file of C++}

        try:
            keys = TASK_PARTS[self.current_task_]
        except KeyError:
            raise ValueError(f"Unknown task:{self.current_task_}")
        
        sections = []
        for key in keys:
            sections.append(f"## {key}\n{inputs[key]}")
        return "\n\n".join(sections)


    def check_size(self, prompt, max_tokens):
        #detect if prompt size is over the limit

        return len(prompt) // 4 <= max_tokens


    def select_llm(self):
        #select what LLM is used to finish task
        if self.current_task_ in ("plan_prompt", "compress_prompt"):
            return "planner"
        return "validation"

    def prepare(self, inputs, max_tokens):
        #build and check the prompt; select the llm
        #return (prompt, llm_type). Notice the user
        #if too big, compress_prompt task first, then re-try
        prompt = self.build_prompt(inputs)
        if not self.check_size(prompt, max_tokens):
            print(f"prompt too big for context window ({max_tokens} tokens)\n \
                  trying compress prompt and retrying...")
            self.current_task_ = "compress_prompt"
            compress_inputs = dict(inputs)
            compress_inputs["prompt"]  = prompt
            prompt = self.build_prompt(compress_inputs)

        return prompt, self.select_llm()
