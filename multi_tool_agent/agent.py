# from google.adk.agents import Agent

# def generate_script(topic: str, feature: str) -> dict:
#     """
#     Generates a YouTube Shorts-style Hinglish script about a tech feature.

#     Args:
#         topic (str): The general tech topic (e.g., WhatsApp, GitHub).
#         feature (str): The specific feature to explain (e.g., Pull Request).

#     Returns:
#         dict: Contains status and the script text.
#     """
#     prompt = f"""
# Write a YouTube Shorts-style script (under 60 seconds) with two Delhi college students, Nik & Sid, casually discussing "{feature}" in "{topic}".

# Instructions:
# 🗣 Use chill Hinglish tone (e.g., "bhai", "scene kya hai", "sach me?", "mast chiz hai").
# 💬 Only dialog between Nik and Sid — no narration.
# 🎭 Show emotion in lines (e.g., excited, confused).
# 📹 Format into timestamps like: (0-5 sec), (5-15 sec), etc.
# 😂 Make it funny, casual, and relatable to college students.
# """

#     return {
#         "status": "success",
#         "script": prompt  # The agent will fill in the Gemini LLM response
#     }

# # Root Agent definition (model handles tool prompts)
# root_agent = Agent(
#     name="Delhi_Tech_Dost",
#     # model = "gemini-2.0-flash",
#     model="gemini-1.5-flash",  # This is all you need to define the model
#     description="An AI agent that explains tech features in a Hinglish YouTube Shorts format.",
#     instruction="You're Nik and Sid — chill Delhi students. Create funny, Hinglish YouTube Shorts-style convos about tech topics.",
#     tools=[generate_script],  # ADK will auto-handle LLM prompting from tool output
# )


from google.adk.agents import Agent
from typing import Dict

# ==== TOOL DEFINITIONS ====

def understand_project(idea: str) -> Dict:
    return {
        "status": "understood",
        "breakdown": f"""
Understand the idea: "{idea}".

🎯 Goal:
- Identify whether it's a full-stack app, AI-integrated tool, or utility.
- Determine necessary features.
- Think like a senior developer and product manager combined.

📦 Output: JSON with 'features', 'techStack', 'pages', 'APIs', and 'dbModels'.
"""
    }

def design_architecture(breakdown: str) -> Dict:
    return {
        "status": "architecture_ready",
        "design": f"""
Based on this project breakdown:
{breakdown}

📐 Create full-stack architecture:
- MERN + Next.js 14 App Router
- Pinecone (if needed), FastAPI, LangChain, LLM APIs
- MongoDB schema or SQL table models

Output:
- Folder structure
- API flow
- UI components
- Data flow
"""
    }

def generate_code(design: str) -> Dict:
    return {
        "status": "code_generated",
        "code_request": f"""
You are a senior-level full-stack engineer.

🧱 Given this system design:
{design}

Write complete modular code for:
1. Frontend (Next.js 14, App Router, Tailwind)
2. Backend (Node/FastAPI)
3. MongoDB or SQL models
4. API routes
5. Utility scripts
6. Auth & AI logic (if needed)

Include code comments and structure as production-ready.
"""
    }

def review_and_improve(code: str) -> Dict:
    return {
        "status": "review_complete",
        "review_task": f"""
🕵️‍♂️ As a senior code reviewer:
1. Review the code below.
2. Suggest improvements (performance, security, modularity).
3. Make changes directly.

Code to review:
{code}
"""
    }

# ==== AGENT HIERARCHY ====

code_reviewer = Agent(
    name="ReviewerAgent",
    model="gemini-1.5-flash",
    description="Senior engineer reviewing and improving final code.",
    instruction="Analyze the code and improve it for production use.",
    tools=[review_and_improve]
)

code_generator = Agent(
    name="CodeAgent",
    model="gemini-1.5-pro",
    description="Writes complete frontend and backend code.",
    instruction="Write complete production-grade code based on system design.",
    tools=[generate_code],
    subagents=[code_reviewer]
)

architect = Agent(
    name="ArchitectAgent",
    model="gemini-1.5-pro",
    description="Breaks down the project and designs system architecture.",
    instruction="Design the architecture of a full MERN/Next.js/Python app.",
    tools=[design_architecture],
    subagents=[code_generator]
)

project_manager = Agent(
    name="ProjectManagerAgent",
    model="gemini-1.5-pro",
    description="Understands the project idea and coordinates all tasks.",
    instruction="You are a senior-level PM and developer. Convert ideas into structured projects.",
    tools=[understand_project],
    subagents=[architect]
)

# ==== STARTER FUNCTION ====

def build_project(idea: str):
    return project_manager.invoke({"idea": idea})
