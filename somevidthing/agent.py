from google.adk.agents import Agent, run
from typing import Dict

# 🛠 Worker Agent: Generates the raw script
def worker_generate_script(topic: str, feature: str, audience: str = "MERN developer") -> Dict:
    """
    Worker Agent that creates an initial script explaining a tech feature.
    """
    prompt = f"""
You're a highly experienced AI content generator for tech topics.

🎯 Audience: {audience}
🧠 Topic: {topic}
🔍 Feature: {feature}
🎬 Format: YouTube Shorts-style (dialogue between two friends)
💬 Tone: Hinglish, fun, casual, but informative
⌛ Duration: < 60 seconds
🧪 Include:
- relatable analogy
- practical use case
- sample code snippet (if relevant)
- timestamps (0–5s, 5–15s, ...)
"""

    return {
        "status": "success",
        "draft_script": prompt
    }

# 🧠 Reviewer Agent: Adds improvements, ensures coherence, jokes, flow
def reviewer_refine_script(draft_script: str) -> Dict:
    """
    Reviewer Agent that improves flow, adds humor, ensures timing and accuracy.
    """
    prompt = f"""
You're a senior tech content editor.

📝 Task: Refine the following draft into an engaging script.
📈 Improve:
- humor balance
- Hinglish tone authenticity
- analogy clarity
- timestamp pacing
- code placement and readability
✅ Keep script < 60 seconds
---

Script to review:
{draft_script}
"""
    return {
        "status": "success",
        "final_script": prompt
    }

# 🧑‍💼 Manager Agent: Coordinates generation and review
manager_agent = Agent(
    name="TechContent_Manager",
    model="gemini-1.5-pro",
    instruction="You're a content lead managing a team. First get the draft from worker, then pass to reviewer. Return final polished script.",
    tools=[worker_generate_script, reviewer_refine_script]
)

# 🧪 Example Run
if __name__ == "__main__":
    result = run(
        agent=manager_agent,
        input={
            "topic": "Pinecone",
            "feature": "Vector Indexing",
            "audience": "MERN stack developers"
        }
    )

    print("\n✅ Final Script:\n")
    print(result["final_script"])
