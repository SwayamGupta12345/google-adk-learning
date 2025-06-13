# agent_pipeline_adk.py

# ✅ Optional LiteLLM import (if you plan to use it later)
from google.adk.models.lite_llm import LiteLlm

import os
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# ✅ Sub-Agent Definitions

# Agent 1: Code Writer
code_writer_agent = LlmAgent(
    name="CodeWriterAgent",
    model="gemini-1.5-flash",
    tools=[],
    instruction="""
You are a Python Code Generator.
Based *only* on the user's request, write Python code that fulfills the requirement.
Output *only* the complete Python code block, enclosed in triple backticks ```python ... ```.
Do not add any other text.
""",
    description="Writes initial Python code based on a specification.",
    output_key="generated_code"
)

# Agent 2: Code Reviewer
code_reviewer_agent = LlmAgent(
    name="CodeReviewerAgent",
    model="gemini-1.5-flash",
    tools=[],
    instruction="""
You are an expert Python code reviewer.
Here is the code to review:

```python
{generated_code}
Review Criteria:

Correctness

Readability (PEP8)

Efficiency

Edge-case handling

Best practices

Provide feedback as a concise bullet list.
If no major issues are found, reply with: No major issues found.
""",
description="Reviews code and provides feedback.",
output_key="review_comments"
)

#Agent 3: Code Refactorer
code_refactorer_agent = LlmAgent(
name="CodeRefactorerAgent",
model="gemini-1.5-flash",
tools=[],
instruction="""
You are a Python Code Refactoring AI.

Original code:

{generated_code}
Review comments:
{review_comments}

Refactor the code based on the feedback.
If the comment says "No major issues found", return the original code unchanged.
Output only the final, refactored code block enclosed in triple backticks (python ... ).
""",
description="Refactors code based on review comments.",
output_key="refactored_code"
)

# Workflow: Sequential Agent Pipeline
code_pipeline_agent = SequentialAgent(
name="CodePipelineAgent",
sub_agents=[code_writer_agent, code_reviewer_agent, code_refactorer_agent],
description="Pipeline: write → review → refactor code."
)

# Required by ADK: root_agent must be defined
root_agent = code_pipeline_agent

# ✅ Runner Setup
SESSION_SERVICE = InMemorySessionService()
runner = Runner(
agent=root_agent,
app_name="local_code_pipeline",
session_service=SESSION_SERVICE
)

# ✅ Pipeline Execution Function
def run_pipeline(user_request: str) -> str:
 """Sends the user request through the pipeline and returns final refactored code."""
 content = types.Content(role="user", parts=[types.Part(text=user_request)])
 final = None

 for event in runner.run(user_id="user_1", session_id="session_1", new_message=content):
    if event.is_final_response():
        final = event.content.parts[2].text
        
        return final
# ✅ Example usage
if __name__ == "__main__":
    prompt = "Write a Python function to compute the factorial of a number recursively."
    result = run_pipeline(prompt)
    print("\nFinal Refactored Code:\n")
    print(result)


